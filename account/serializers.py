# account/serializers.py

from django.contrib.auth.models import User # Or your CustomUser model
from rest_framework import serializers
from .models import Profile

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the User profile object.
    Used for retrieving and updating the authenticated user's information.
    """
    # Explicitly define fields from the related User model
    username = serializers.CharField(source='user.username', required=False)
    first_name = serializers.CharField(source='user.first_name', required=True)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', read_only=True) # Good practice to make email read-only here

    class Meta:
        model = Profile
        # List the fields from the Profile model AND the new explicit fields
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'location',
            'birth_date',
            'phone_number',
        )
        read_only_fields = ('id',)

        # extra_kwargs is not needed for the user fields anymore since we defined them above
        extra_kwargs = {
            'bio': {'required': False},
            'location': {'required': False},
            'birth_date': {'required': False},
            'phone_number': {'required': True},
        }

    # You also need to override the update method to save the related User model data
    def update(self, instance, validated_data):
        # Pop the user data out of the validated_data
        user_data = validated_data.pop('user', {})

        # Update the User model fields if they exist in the data
        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.username = user_data.get('username', user.username)
        user.save()

        # Update the Profile model fields (the default behavior)
        # This will call the parent class's update method
        return super().update(instance, validated_data)