from django.urls import path
from .views import schoolDetails

urlpatterns = [
    path("", schoolDetails, name="detailView")
]