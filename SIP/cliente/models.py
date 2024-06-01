from django.db import models

# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    identity = models.CharField(max_length=255)
    phone_contact = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    