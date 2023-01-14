from django.urls import path

from core.views import CreateUser

urlpatterns = [
    path('signup', CreateUser.as_view()),
]
