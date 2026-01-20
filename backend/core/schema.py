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
        try:
            # Organization-scoped filtering
            return Project.objects.filter(organization_id=organization_id).prefetch_related('tasks')
        except Project.DoesNotExist:
             # Return None (GraphQL handles null)
            return None
        except ValueError:
            raise Exception("Invalid ID format") 
        # Let other exceptions crash - they're bugs!   
        
    def resolve_project(self, info, id):
        try:
          return Project.objects.prefetch_related('tasks__comments').get(id=id)
        except Project.DoesNotExist:
             # Return None (GraphQL handles null)
            return None
        except ValueError:
            raise Exception("Invalid ID format") 

# prefetch_related avoids n+1 query problem by fetching related objects in a single query

class Mutation(graphene.ObjectType):
    pass