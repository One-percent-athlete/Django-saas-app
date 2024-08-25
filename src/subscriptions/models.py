from django.contrib.auth.models import Group, Permission
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

User = settings.AUTH_USER_MODEL

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
    
class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} - {self.subscription}"
    
def user_sub_post_save(sender, instance, *args, **kwargs):
    user_sub_instance = instance
    user = user_sub_instance.user
    subscription_obj = user_sub_instance.subscription
    groups = subscription_obj.groups.all()
    user.groups.set(groups)

post_save.connect(user_sub_post_save, sender=UserSubscription)