from django.db import models
from users.models import User


class ChatGroup(models.Model):
    name = models.CharField(max_length=255)
    interest = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'group')


class GroupInvitation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("declined", "Declined")
    ]
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_invitations")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_invitations")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    sent_at = models.DateTimeField(auto_now_add=True)
