from django.db import models
from django.contrib.auth.models import Group, Permission


SUB_PERMS = [
        ("free", "Free Perm"),
        ("basic", "Basic Perm"),
        ("advance", "Advance Perm"),
        ("pro", "Pro Perm"),
    ]


class Subscription(models.Model):

    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission, 
        limit_choices_to={
            "content_type__app_label": "subscriptions", 
            "codename__in": [x[0] for x in SUB_PERMS]
        }
    )

    class Meta:
        permissions = SUB_PERMS

    def __str__(self):
        return self.name