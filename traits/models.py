from groups.models import Group
from django.db import models; 
from django.apps import apps

class Trait(models.Model):
    name = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return f"<[{self.id}] - ({self.name})>"