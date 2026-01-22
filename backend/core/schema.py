import graphene
from graphene_django import DjangoObjectType
from .models import Project, Task, Organization, TaskComment

class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'slug', 'contact_email', 'created_at', 'last_updated_at')
        
    # an org has many projects so we define projects as a TYPE- list of ProjectType, coz in resolver it's used so we define type
    projects = graphene.List(lambda: ProjectType)
    
    def resolve_projects(self, info):
        return self.projects.all()

class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'status', 'due_date', 'organization', 'created_at', 'last_updated_at')
        
    # a project has many tasks so we define tasks as a TYPE- list of TaskType, coz in resolver it's used so we define type
    tasks = graphene.List(lambda: TaskType)
    
    def resolve_tasks(self, info):
        return self.tasks.all()

class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'assignee_email', 'due_date', 'project', 'created_at', 'last_updated_at') 
        
    # a task has many comments so we define comments as a TYPE- list of TaskCommentType, coz in resolver it's used so we define type
    comments = graphene.List(lambda: TaskCommentType)
    
    def resolve_comments(self, info):
        return self.comments.all()

class TaskCommentType(DjangoObjectType):
    class Meta:
        model = TaskComment
        fields = ('id', 'task', 'content', 'author_email', 'created_at', 'last_updated_at') 
        
        
# QUERIES
class Query(graphene.ObjectType):
    # 1. List projects (organization-scoped)
    projects = graphene.List(
        ProjectType,
        organization_id=graphene.ID(required=True)
    )
    
    # 2. Get project with tasks
    project = graphene.Field(
        ProjectType,
        id=graphene.ID(required=True)
    )
    
    def resolve_projects(self, info, organization_id):
        # .filter() returns empty list if no matches, no exception
        return Project.objects.filter(
            organization_id=organization_id
        ).prefetch_related('tasks')
          
        
    def resolve_project(self, info, id):
        try:
          return Project.objects.prefetch_related('tasks__comments').get(id=id)
        except Project.DoesNotExist:
             # Return None (GraphQL handles null)
            return None
        except ValueError:
            raise Exception("Invalid ID format") 
        # Let other exceptions crash - they're bugs! 
# prefetch_related avoids n+1 query problem by fetching related objects in a single query

# MUTATIONS
class CreateProject(graphene.Mutation):
    class Arguments:
        organization_id = graphene.ID(required=True)
        name = graphene.String(required=True)
        description = graphene.String()
        status = graphene.String(default_value="ACTIVE")
        due_date = graphene.Date()
    
    project = graphene.Field(ProjectType)
    
    def mutate(self, info, organization_id, name, **kwargs):
        # Check organization exists
        if not Organization.objects.filter(id=organization_id).prefetch_related('tasks').exists():
            raise Exception(f"Organization {organization_id} not found")
        
        # Validate name
        if not name or not name.strip():
            raise Exception("Project name cannot be empty")
        
        project = Project(
            organization_id=organization_id,
            name=name.strip(),
            **kwargs
        )
        project.save()
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
        # Check project exists
        try:
            project = Project.objects.prefetch_related('tasks__comments').get(id=id)
        except Project.DoesNotExist:
            raise Exception(f"Project {id} not found")
        
        # Validate name if provided
        if 'name' in kwargs and kwargs['name']:
            if not kwargs['name'].strip():
                raise Exception("Project name cannot be empty")
            kwargs['name'] = kwargs['name'].strip()
        
        # Update fields
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
        # Check project exists
        if not Project.objects.filter(id=project_id).prefetch_related('tasks__comments').exists():
            raise Exception(f"Project {project_id} not found")
        
        # Validate title
        if not title or not title.strip():
            raise Exception("Task title cannot be empty")
        
        task = Task(
            project_id=project_id,
            title=title.strip(),
            **kwargs
        )
        task.save()
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
        # Check task exists
        try:
            task = Task.objects.prefetch_related('comments').get(id=id)
        except Task.DoesNotExist:
            raise Exception(f"Task {id} not found")
        
        # Validate title if provided
        if 'title' in kwargs and kwargs['title']:
            if not kwargs['title'].strip():
                raise Exception("Task title cannot be empty")
            kwargs['title'] = kwargs['title'].strip()
        
        # Update fields
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
        # Check task exists
        if not Task.objects.filter(id=task_id).prefetch_related('comments').exists():
            raise Exception(f"Task {task_id} not found")
        
        # Validate content
        if not content or not content.strip():
            raise Exception("Comment cannot be empty")
        
        # Basic email validation
        if not author_email or "@" not in author_email:
            raise Exception("Valid email is required")
        
        comment = TaskComment(
            task_id=task_id,
            content=content.strip(),
            author_email=author_email.strip()
        )
        comment.save()
        return AddComment(comment=comment)


class Mutation(graphene.ObjectType):
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    add_comment = AddComment.Field()