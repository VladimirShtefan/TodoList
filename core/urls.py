from django.urls import path

from core.views import CreateUserView, UserLoginView

urlpatterns = [
    path('signup', CreateUserView.as_view(), name='user-signup'),
    path('login', UserLoginView.as_view(), name='user-login'),
]
