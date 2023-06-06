from django.db import models


from django.db import models

class Contact(models.Model):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    
    LINK_PRECEDENCE_CHOICES = [
        (PRIMARY, 'Primary'),
        (SECONDARY, 'Secondary'),
    ]

    phoneNumber = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    linkedId = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    linkPrecedence = models.CharField(max_length=10, choices=LINK_PRECEDENCE_CHOICES, default=PRIMARY)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True)

    def __str__(self):
        return f"Contact: {self.id}"
