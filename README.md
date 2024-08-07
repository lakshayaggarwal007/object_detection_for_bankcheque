# Bank Cheque Object Detection API

## Overview

This project provides an API for object detection on bank cheques, extracting key information such as date, amount, account number, and payee name. It uses the YOLOv8 model for object detection and includes several routes to interact with the API, upload images, and retrieve detection results.

## Features

- **Object Detection on Bank Cheques**: Automatically detects and extracts essential information from bank cheques.
- **Image Upload API**: Upload images via an API endpoint for processing.
- **Image Details Retrieval**: View the detection results for individual images or all images processed by the API.
- **Folder Monitoring with Watchdog**: Automatically processes images added to a specific folder.
- **Zero-Shot Detection**: Uses the Florence-2 VLM model to perform object detection based on a provided image and prompt.

## Installation

1. **Create a virtual environment**:
    - **Windows**:
        ```bash
        python -m venv venv
        venv\\Scripts\\activate
        ```
    - **Linux/MacOS**:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

2. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

3. **Install required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply database migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

The project includes the following API routes:

- **Upload Image**: Upload a new image for processing.
    ```bash
    POST /upload/
    ```
    **Body Parameters**:
    - `image`: The image file to be processed.
    - `image_name`: A unique name for the image.
    
    **Response**:
    ```json
    {
        "message": "Image processed successfully",
        "result": {
            "name": "20230102170101005F",
            "count": 5,
            "coordinates": [
                [
                    [
                        608.5472412109375,
                        38.932518005371094,
                        772.8692016601562,
                        65.14527893066406
                    ]
                ],
                [
                    [
                        59.948097229003906,
                        74.37309265136719,
                        175.94265747070312,
                        105.37074279785156
                    ]
                ],
                [
                    [
                        607.0962524414062,
                        147.72447204589844,
                        681.300048828125,
                        173.81915283203125
                    ]
                ],
                [
                    [
                        130.07003784179688,
                        195.60968017578125,
                        211.24278259277344,
                        212.33128356933594
                    ]
                ],
                [
                    [
                        187.34487915039062,
                        331.81158447265625,
                        577.23046875,
                        355.43511962890625
                    ]
                ]
            ],
            "annotated_image": "/media/annotated/annotated_20230102170101005f.jpg"
        }
    }
    ```
    You can click on the `annotated_image` link in the response to view the annotated image.

- **Get Image Details**: Retrieve the details of a processed image by name.
    ```bash
    GET /image/<str:image_name>/
    ```
    **Example**: 
    ```bash
    http://127.0.0.1:8000/api/image/20230102170101005F
    ```
    This endpoint returns the details of a specific image, including the detected objects and the annotated image URL.

- **Get All Image Details**: Retrieve the details of all processed images.
    ```bash
    GET /images/
    ```
    This endpoint returns details of all images that have been processed by the API.

## Folder Monitoring with Watchdog

The project includes a folder watcher that automatically detects when a new image is added to a specified folder name **"images"** that is in project directory. Once an image is detected, it is processed automatically, and the extracted data is stored.

## Zero-Shot Detection

The project also supports zero-shot detection using the Florence-2 VLM model. This allows object detection based on a provided image and a prompt without the need for prior training on specific object categories.

If it does not work on local that might be because you don't have cuda or torch that is cuda compatible ,you can try running it on colab as it provide 15gb gpu

To run zero-shot detection, execute the `Zero_shot_mode.py` file in another terminal and change the image and prompt based on requirement:
```bash
python Zero_shot_mode.py
```