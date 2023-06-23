from django.db import models
from uuid import uuid4

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=256, null=False, unique=True)

    def __str__(self):
        return f"This is the user {self.username}"

class Task(models.Model):
    created = "CR"
    in_progress = "IP"
    finished = "FD"

    STATUS_OF_TASKS = [
        (created, "Created"),
        (in_progress, "In Progress"),
        (finished, "Finished"),
    ]
    title = models.CharField(max_length=256, null=False)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_OF_TASKS, default=created)
    due_date = models.DateField(null=False)
    last_modified = models.DateField(auto_now=True, editable=False)
    start_date = models.DateField(auto_now_add=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return f"The task '{self.title}' was created by {self.user.username}"
