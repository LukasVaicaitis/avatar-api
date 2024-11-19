from django.urls import path
from .views import PhotoUploadView, PhotoListView, PhotoDeleteView, UserRegisterView, SaveProjectView, ProjectListView, GetImageByIdView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('upload-photo/', PhotoUploadView.as_view(), name='upload-photo'),
    path('photos/', PhotoListView.as_view(), name='photo_list'),
    path('photos/delete/<int:pk>/', PhotoDeleteView.as_view(), name='photo-delete'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('save-project/', SaveProjectView.as_view(), name='save-project'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('get-image/<int:photo_id>/', GetImageByIdView.as_view(), name='get_image_by_id'),
]