from django.db import IntegrityError
from rest_framework import serializers
from .models import Follower

class FollowerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        model = Follower
        fields = [
            'id', 'owner', 'created_at', 'followed', 'followed_name'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            error_message = str(e)
            if 'unique constraint' in error_message.lower():
                raise serializers.ValidationError({'detail': 'You are already following this user.'})
            else:
                raise serializers.ValidationError({'detail': 'An error occurred while trying to follow the user.'})