from django.contrib.auth.models import Group, Permission
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

from helpers import billing

User = settings.AUTH_USER_MODEL
ALLOW_CUSTOM_GROUPS = True

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

    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        permissions = SUB_PERMS

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not stripe_id:
            stripe_id = billing.create_product(name=self.name, metadata={'subscription_plan__id': self.id}, raw=False)
            self.stripe_id = stripe_id
        
        super().save(*args, **kwargs)
    
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
    groups_ids = []
    if subscription_obj is not None:
        groups = subscription_obj.groups.all()
        groups_ids = groups.values_list('id', flat=True)
    if not ALLOW_CUSTOM_GROUPS:
        user.groups.set(groups)
    else:
        subs_qs = Subscription.objects.filter(active=True)
        if subscription_obj is not None:
            subs_qs = subs_qs.exclude(id=subscription_obj.id)
        subs_groups = subs_qs.values_list('gourps__id', flat=True)
        subs_groups_set = set(subs_groups)

        current_groups = user.groups.all().values_list('id', flat=True)
        groups_ids_set = set(groups_ids)
        current_groups_set = set(current_groups) - subs_groups_set
        final_groups_ids = list(groups_ids_set | current_groups_set)
        user.groups.set(final_groups_ids)

post_save.connect(user_sub_post_save, sender=UserSubscription)