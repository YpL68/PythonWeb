from django.db import models


class FinCategory(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False, unique=True, verbose_name="Name")
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name="Description")
    created_on = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.name
