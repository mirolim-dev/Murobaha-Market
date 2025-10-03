from django.shortcuts import render
from rest_framework import generics, permissions

# from local apps
from .models import Profile
from .serializers import UserProfileSerializer

class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Manage the authenticated user's profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access this view

    def get_object(self):
        """
        Retrieve and return the authenticated user.
        We override this method to ensure the user gets their OWN profile, not someone else's.
        """
        return self.request.user