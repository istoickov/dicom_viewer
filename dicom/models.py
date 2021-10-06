from django.db import models


class DicomImages(models.Model):
    file = models.FileField()
    uid = models.TextField()
    response = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uid} - {self.response}"
