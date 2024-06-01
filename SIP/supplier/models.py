from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    identity = models.CharField(max_length=255)

    def __str__(self):
        return self.name
