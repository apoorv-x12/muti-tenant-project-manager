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