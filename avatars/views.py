# Standard imports
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User

# TP imports
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

# Project specific
from .models import Photo, Project
from .serializers import PhotoSerializer, ProjectSerializer

class PhotoUploadView(generics.CreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class PhotoListView(generics.ListAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            queryset = Photo.objects.filter(user=self.request.user)
            return queryset
        except Exception as e:
            raise

class PhotoDeleteView(generics.DestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            # Fetching the photo using pk and ensuring it belongs to the current user
            photo = Photo.objects.get(pk=self.kwargs['pk'], user=self.request.user)
            return photo
        except Photo.DoesNotExist:
            raise

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except Exception as e:
            raise

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            return user
        except Exception as e:
            raise

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            except Exception as e:
                raise
        return Response(serializer.errors, status=400)

class SaveProjectView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):

        name = request.data.get('name')
        photo = request.data.get('photo_id')
        scene_data = request.data.get('scene_data')

        if not name or not photo:
            raise ValidationError("Project name and photo are required.")

        try:
            photo = Photo.objects.get(id=photo, user=request.user)
        except Photo.DoesNotExist:
            raise ValidationError("Invalid photo ID or unauthorized.")

        if not scene_data or not isinstance(scene_data, dict):
            raise ValidationError("Scene data is required and must be a valid JSON object.")

        project = Project.objects.create(
            user=request.user,
            name=name,
            photo=photo,
            scene_data=scene_data
        )
        
        serializer = self.get_serializer(project)
        return Response(serializer.data, status=201)

class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            queryset = Project.objects.filter(user=self.request.user)
            return queryset
        except Exception as e:
            raise

class GetImageByIdView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, photo_id, *args, **kwargs):
        try:
            photo = Photo.objects.get(id=photo_id, user=request.user)
            image_url = photo.image.url      

            if not image_url:
                raise ValidationError("Image URL not found for this photo.")
            
            scheme = request.scheme  # 'http' or 'https'
            domain = get_current_site(request).domain
            full_image_url = f"{scheme}://{domain}{image_url}"        

            return Response({'image_url': full_image_url}, status=200)
        except Photo.DoesNotExist:
            raise ValidationError("Photo not found or doesn't belong to the user.")
        except Exception as e:
            raise