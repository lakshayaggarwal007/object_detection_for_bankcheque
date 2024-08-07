from django.urls import path
from .views import UploadImageView, ImageDetailView, AllImagesDetailView

urlpatterns = [
    path('upload/', UploadImageView.as_view(), name='upload_image'),
    path('image/<str:image_name>/', ImageDetailView.as_view(), name='image_detail'),
    path('images/', AllImagesDetailView.as_view(), name='all_images_details'),  # New route for all images
]
