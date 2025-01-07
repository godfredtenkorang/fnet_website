from django.db import models

# Create your models here.
class SMSLog(models.Model):
    recipients = models.TextField()
    message = models.TextField()
    status = models.CharField(max_length=20, null=True, blank=True)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message