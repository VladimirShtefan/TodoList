from django.urls import path

from bot.views import VerificationCodeView


urlpatterns = [
    path('verify', VerificationCodeView.as_view(), name='bot_verify'),
]
