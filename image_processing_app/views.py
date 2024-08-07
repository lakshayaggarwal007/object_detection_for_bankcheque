from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import os
import json
from django.utils.text import slugify
from PIL import Image, ImageDraw
from ultralytics import YOLO

# Helper function to process the image with YOLOv8
def process_image_with_yolov8(image, image_name, request=None):
    # Load the YOLOv8 model
    model = YOLO(r'image_processing_app\models\best.pt')  # Load the pre-trained YOLOv8 model

    # Slugify the image name to make it URL-friendly
    slugified_image_name = slugify(image_name)

    # Check if `image` is a file object or a file path
    if hasattr(image, 'chunks'):
        # If image is uploaded via API, save the uploaded image
        image_path = os.path.join("images", f"{slugified_image_name}.JPG")
        with open(image_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
    else:
        # If image is already a file path, use it directly
        image_path = image

    # Run YOLOv8 detection
    results = model.predict(image_path, imgsz=800, conf=0.25, max_det=5, save_crop=True, exist_ok=True, project="TextExtract/temp_folder", name="crop_files", device='cpu')

    # Process the results
    object_count = len(results[0].boxes)
    coordinates = [box.xyxy.tolist() for box in results[0].boxes]

    # Annotate the image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    for box in coordinates:
        draw.rectangle(box[0], outline="red", width=3)

    # Define the annotated image path relative to the MEDIA_ROOT
    annotated_image_rel_path = f"annotated/annotated_{slugified_image_name}.jpg"
    annotated_image_path = os.path.join(settings.MEDIA_ROOT, annotated_image_rel_path)
    
    # Save the annotated image
    os.makedirs(os.path.dirname(annotated_image_path), exist_ok=True)
    img.save(annotated_image_path)

    # Get the full URL for the annotated image
    if request:
        annotated_image_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{annotated_image_rel_path}".replace("\\", "/"))
    else:
        annotated_image_url = f"{settings.MEDIA_URL}{annotated_image_rel_path}".replace("\\", "/")

    # Create the result dictionary
    result = {
        "name": image_name,
        "count": object_count,
        "coordinates": coordinates,
        "annotated_image": annotated_image_url  # Full URL path
    }

    return result


class UploadImageView(APIView):
    def post(self, request):
        image = request.FILES.get('image')
        image_name = request.data.get('image_name')

        if not image:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not image_name:
            return Response({"error": "No image name provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        result_path = os.path.join(settings.MEDIA_ROOT, 'results.json')
        existing_data = {}

        if os.path.exists(result_path):
            with open(result_path, 'r') as f:
                existing_data = json.load(f)

            if image_name in existing_data:
                return Response({
                    "message": "Image name already exists",
                    "data": existing_data[image_name]
                }, status=status.HTTP_200_OK)
        
        # Process the image and get the result
        result = process_image_with_yolov8(image, image_name)
        
        # Save the result to the JSON file
        existing_data[image_name] = result
        with open(result_path, 'w') as f:
            json.dump(existing_data, f)
        
        return Response({"message": "Image processed successfully", "result": result}, status=status.HTTP_201_CREATED)




class ImageDetailView(APIView):
    def get(self, request, image_name):
        result_path = os.path.join(settings.MEDIA_ROOT, 'results.json')
        if not os.path.exists(result_path):
            return Response({"error": "Results file not found"}, status=status.HTTP_404_NOT_FOUND)

        with open(result_path, 'r') as f:
            results = json.load(f)
        
        if image_name in results:
            return Response(results[image_name], status=status.HTTP_200_OK)
        else:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
        
class AllImagesDetailView(APIView):
    def get(self, request):
        result_path = os.path.join(settings.MEDIA_ROOT, 'results.json')
        
        if not os.path.exists(result_path):
            return Response({"error": "Results file not found"}, status=status.HTTP_404_NOT_FOUND)
        
        with open(result_path, 'r') as f:
            results = json.load(f)
        
        # Exclude coordinates from the results
        modified_results = {key: {k: v for k, v in value.items() if k != 'coordinates'} for key, value in results.items()}
        
        return Response(modified_results, status=status.HTTP_200_OK)
