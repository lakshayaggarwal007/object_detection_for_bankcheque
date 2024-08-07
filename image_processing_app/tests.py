from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class ImageUploadTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.upload_url = reverse('upload_image')

    def test_image_upload(self):
        # Create a dummy image file
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

        # Post the image
        response = self.client.post(self.upload_url, {'image': image}, format='multipart')

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('image_id', response.data)

    def tearDown(self):
        # Cleanup media files
        media_root = os.path.join(os.getcwd(), 'media')
        for file in os.listdir(media_root):
            file_path = os.path.join(media_root, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
