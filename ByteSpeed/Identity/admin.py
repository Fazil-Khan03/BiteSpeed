from django.contrib import admin
from .models import Contact
''''
  phoneNumber = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    linkedId = models.IntegerField(null=True)
    linkPrecedence = models.CharField(
        max_length=10,
        choices=choices,
        default='primary'
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True)

'''

# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Contact._meta.get_fields()]
    list_display = ['phoneNumber', 'email', 'linkedId', 'linkPrecedence']