from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/booking/", views.submit_booking, name="submit_booking"),
    path("api/ai/chat/", views.ai_chat, name="ai_chat"),
    path("health/", views.health_check, name="health_check"),
]
