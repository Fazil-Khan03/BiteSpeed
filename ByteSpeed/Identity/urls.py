from django.urls import path
from .views import ContactView


urlpatterns = [
    path('identity/', ContactView.as_view()),
]