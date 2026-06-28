from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("projects/", views.projects, name="projects"),
    path("pricing/", views.pricing, name="pricing"),
    path("reviews/", views.reviews, name="reviews"),
    path("faq/", views.faq, name="faq"),
    path("book/", views.book, name="book"),
    path("contact/", views.contact, name="contact"),
    path("api/booking/", views.submit_booking, name="submit_booking"),
    path("api/ai/chat/", views.ai_chat, name="ai_chat"),
    path("health/", views.health_check, name="health_check"),
]
