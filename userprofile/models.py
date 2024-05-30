from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=100, null=True)
    address2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50,  null=True)
    state = models.CharField(max_length=50,  null=True)
    country = models.CharField(max_length=50,  null=True)
    zipcode = models.CharField(max_length=10,  null=True)
    phone = models.CharField(max_length=20,  null=True)
    address_confirmed = models.BooleanField(default=False)  # Add the address_confirmed field

    def __str__(self):
        return f"{self.address1}, {self.city}, {self.state}, {self.country}, {self.zipcode}"

    class Meta:
        verbose_name_plural = "Addresses"
