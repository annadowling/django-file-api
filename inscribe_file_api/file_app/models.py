from django.db import models

class File(models.Model):
    file = models.FileField(upload_to='files/')
    category = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)

    def __str__(self):
        return self.file.name
