from django.urls import path, include
from rest_framework import routers

from EvenAPI.views import EventViewSet

router = routers.DefaultRouter()
router.register(r"event", EventViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "eventApi"