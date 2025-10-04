from django.urls import path
from apis.views import (
    UserProfileView,
)
    
urlpatterns = [
    path("profile", UserProfileView.as_view(), name="user-profile"),
]