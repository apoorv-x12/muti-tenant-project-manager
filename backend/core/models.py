from django.db import models

class Organization(models.Model):
    name=models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    contact_email=models.EmailField()
    created_at=models.DateTimeField(auto_now_add=True)
    last_updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
class Project(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('ON_HOLD', 'On Hold'),
    ]
    
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE,
        related_name='projects'
    ) # delete all records here if organization is deleted
    name=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='ACTIVE'
    )
    due_date=models.DateField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    last_updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]
    
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='TODO'
    )
    assignee_email = models.EmailField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
class TaskComment(models.Model):
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    author_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Comment by {self.author_email} on {self.task.title}"