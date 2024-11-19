from rest_framework import serializers
from .models import Photo
from .models import Project

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'user', 'image', 'uploaded_at']
        read_only_fields = ['id', 'user', 'uploaded_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'user', 'name', 'created_at', 'photo', 'scene_data']
        read_only_fields = ['id', 'created_at']