import graphene
from graphene_django import DjangoObjectType
from .models import Project, Task, Organization, TaskComment


# ======================
# GRAPHQL TYPES
# ======================

class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "slug",
            "contact_email",
            "created_at",
            "last_updated_at",
        )
   # an org has many projects so we define projects as a TYPE- list of ProjectType, coz in resolver it's used so we define type
    projects = graphene.List(lambda: ProjectType)

    def resolve_projects(self, info):
        return self.projects.all()


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "description",
            "status",
            "due_date",
            "organization",
            "created_at",
            "last_updated_at",
        )
   # a project has many tasks so we define tasks as a TYPE- list of TaskType, coz in resolver it's used so we define type
    tasks = graphene.List(lambda: TaskType)

    def resolve_tasks(self, info):
        return self.tasks.all()


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "assignee_email",
            "due_date",
            "project",
            "created_at",
            "last_updated_at",
        )
    # a task has many comments so we define comments as a TYPE- list of TaskCommentType, coz in resolver it's used so we define type
    comments = graphene.List(lambda: TaskCommentType)

    def resolve_comments(self, info):
        return self.comments.all()


class TaskCommentType(DjangoObjectType):
    class Meta:
        model = TaskComment
        fields = (
            "id",
            "task",
            "content",
            "author_email",
            "created_at",
            "last_updated_at",
        )


# ======================
# QUERIES
# ======================

class Query(graphene.ObjectType):
    # List projects (ORG-SCOPED)
    projects = graphene.List(ProjectType)

    # Get single project (ORG-SCOPED)
    project = graphene.Field(ProjectType, id=graphene.ID(required=True))

    def resolve_projects(self, info):
        org = info.context.organization
        if not org:
            raise Exception("X-ORG header required")

        return (
            Project.objects.filter(organization=org)
            .prefetch_related("tasks")
        )

    def resolve_project(self, info, id):
        org = info.context.organization
        if not org:
            raise Exception("X-ORG header required")

        try:
            return Project.objects.prefetch_related(
                "tasks__comments"
            ).get(id=id, organization=org)
        except Project.DoesNotExist:
            return None
# Let other exceptions crash - they're bugs! 
# prefetch_related avoids n+1 query problem by fetching related objects in a single query

# ======================
# MUTATIONS
# ======================

class CreateProject(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        status = graphene.String(default_value="ACTIVE")
        due_date = graphene.Date()

    project = graphene.Field(ProjectType)

    def mutate(self, info, name, **kwargs):
        org = info.context.organization
        if not org:
            raise Exception("X-ORG header required")

        if not name.strip():
            raise Exception("Project name cannot be empty")

        project = Project.objects.create(
            organization=org,
            name=name.strip(),
            **kwargs,
        )

        return CreateProject(project=project)


class UpdateProject(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        status = graphene.String()
        due_date = graphene.Date()

    project = graphene.Field(ProjectType)

    def mutate(self, info, id, **kwargs):
        org = info.context.organization
        if not org:
            raise Exception("X-ORG header required")

        try:
            project = Project.objects.get(id=id, organization=org)
        except Project.DoesNotExist:
            raise Exception("Project not found")

        if "name" in kwargs and kwargs["name"]:
            if not kwargs["name"].strip():
                raise Exception("Project name cannot be empty")
            kwargs["name"] = kwargs["name"].strip()

        for field, value in kwargs.items():
            if value is not None:
                setattr(project, field, value)

        project.save()
        return UpdateProject(project=project)


class CreateTask(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        description = graphene.String()
        status = graphene.String(default_value="TODO")
        assignee_email = graphene.String()
        due_date = graphene.DateTime()

    task = graphene.Field(TaskType)

    def mutate(self, info, project_id, title, **kwargs):
        org = info.context.organization
        if not org:
            raise Exception("X-ORG header required")

        try:
            project = Project.objects.get(
                id=project_id,
                organization=org,
            )
        except Project.DoesNotExist:
            raise Exception("Project not found")

        if not title.strip():
            raise Exception("Task title cannot be empty")

        task = Task.objects.create(
            project=project,
            title=title.strip(),
            **kwargs,
        )

        return CreateTask(task=task)


class UpdateTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
        status = graphene.String()
        assignee_email = graphene.String()
        due_date = graphene.DateTime()

    task = graphene.Field(TaskType)

    def mutate(self, info, id, **kwargs):
        org = info.context.organization
        if not org:
            raise Exception("X-ORG header required")

        try:
            task = Task.objects.select_related("project").get(
                id=id,
                project__organization=org,
            )
        except Task.DoesNotExist:
            raise Exception("Task not found")

        if "title" in kwargs and kwargs["title"]:
            if not kwargs["title"].strip():
                raise Exception("Task title cannot be empty")
            kwargs["title"] = kwargs["title"].strip()

        for field, value in kwargs.items():
            if value is not None:
                setattr(task, field, value)

        task.save()
        return UpdateTask(task=task)


class AddComment(graphene.Mutation):
    class Arguments:
        task_id = graphene.ID(required=True)
        content = graphene.String(required=True)
        author_email = graphene.String(required=True)

    comment = graphene.Field(TaskCommentType)

    def mutate(self, info, task_id, content, author_email):
        org = info.context.organization
        if not org:
            raise Exception("X-ORG header required")

        try:
            task = Task.objects.select_related("project").get(
                id=task_id,
                project__organization=org,
            )
        except Task.DoesNotExist:
            raise Exception("Task not found")

        if not content.strip():
            raise Exception("Comment cannot be empty")

        if "@" not in author_email:
            raise Exception("Valid email required")

        comment = TaskComment.objects.create(
            task=task,
            content=content.strip(),
            author_email=author_email.strip(),
        )

        return AddComment(comment=comment)


class Mutation(graphene.ObjectType):
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    add_comment = AddComment.Field()
