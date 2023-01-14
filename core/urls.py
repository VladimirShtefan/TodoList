from django.urls import path

from core.views import CreateUserView, UserLoginView, UserProfileView

urlpatterns = [
    path('signup', CreateUserView.as_view(), name='user-signup'),
    path('login', UserLoginView.as_view(), name='user-login'),
    path('profile', UserProfileView.as_view(), name='user-profile'),
]
