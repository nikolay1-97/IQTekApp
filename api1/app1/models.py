from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    full_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'
