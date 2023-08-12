from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    DOB = models.DateField()
    address = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    profile_pic = models.ImageField(upload_to='profileimg',null=True)



