from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    recipient = models.ForeignKey(User, related_name='notifications_received', on_delete=models.CASCADE)
    actor = models.ForeignKey(User, related_name='notifications_sent', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)  # Describing the action (e.g., 'liked', 'commented on', etc.)
    
    # Generic relation for the target (the object being acted upon)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')
    
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification from {self.actor} to {self.recipient} about {self.verb} {self.target}"

    class Meta:
        ordering = ['-timestamp']  # To order by the most recent notifications first
