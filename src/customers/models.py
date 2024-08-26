from django.db import models
from django.conf import settings

from helpers import billing

User = settings.AUTH_USER_MODEL

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"
    
    def save(self, *args, **kwargs):
        email = self.user.email
        if not stripe_id:
            if email != "" or email is not None:
                stripe_id = billing.create_customer(email=email, raw=False)
                self.stripe_id = stripe_id
        
        stripe_res = billing.create_customer(raw=True)
        super().save(*args, **kwargs)