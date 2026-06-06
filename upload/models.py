from django.db import models


class UploadedItem(models.Model):
    name = models.CharField(max_length=49)
    date = models.DateTimeField()

    class Meta:
        ordering = ['date', 'name']

    def __str__(self):
        return f'{self.name} ({self.date})'
