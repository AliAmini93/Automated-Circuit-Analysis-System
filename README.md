# Automated Circuit Analysis System
This multifaceted project is comprised of 5 main sections including 2D Image Representation, Electrical Board Detection, IC detection, IC Recognition, and preparing a GUI to automate the entire process.
## 2D Image Representation

### 1. Data Collection
- **Task**: Capture images using a provided platform, ensuring significant overlap for accuracy.
  
![image](https://github.com/AliAmini93/Automated-Circuit-Analysis-System/assets/96921261/e18df852-7dd5-4a06-8767-58e3900542ae)

### 2. Image Preprocessing
- **Task**: Analyze image metadata for camera details and location information.

### 3. Initial Processing - Key Point Detection and Matching
- **Task**: Detect distinct points in each image.
- **Task**: Match these points across overlapping images to identify common areas.

### 4. Point Cloud and Tie Points Generation
- **Task**: Generate a sparse point cloud from matched points.
- **Task**: Identify tie points (points appearing in multiple images) for 3D modeling.

### 5. Calibration and Alignment
- **Task**: Perform camera calibration and refine tie point positions.
- **Task**: Use positional data for model alignment.

### 6. Dense Point Cloud Generation
- **Task**: Create a dense point cloud for detailed representation.

### 7. Surface and Terrain Model Generation
- **Task**: Generate a detailed Surface Model and Terrain Model from the dense point cloud.

### 8. Orthomosaic Creation
- **Task**: Stitch processed images to create an orthomosaic.
- **Task**: Correct perspective distortions for uniform scale and adjust for topography.

### 9. Refinement and Output
- **Task**: Refine the orthomosaic through editing or enhancement.
- **Result**: High-resolution, accurately scaled 2D map.

![compressed_1](https://github.com/AliAmini93/Automated-Circuit-Analysis-System/assets/96921261/2dac1f4c-8ba6-4117-a298-5061f07c2c80)

## Electrical Board Detection

### 1. Board Isolation
- **Task**: Process the image to isolate the electrical board, reducing background presence.

### 2. Image Refinement
- **Result**: Refined image predominantly featuring the electrical board, ready for further analysis.

### 3. Data Augmentation
- **Task**: Apply data augmentation techniques to enhance the pre-trained YOLOv8n model's performance.
- **Purpose**: Generate additional training samples to prevent overfitting and improve model generalization.

### 4. Dataset Description
- **Details**: The dataset includes 742 images of various boards in different colors, sizes, and perspectives.
- **Status**: Actively expanding the dataset with more images. Currently not publicly available.

### 5. Model Performance
- **Note**: The trained model's performance will be showcased below.
- **Model Availability**: The fine-tuned model can be provided upon request.

![FinalIMG](https://github.com/AliAmini93/Electrical-Board-detection/assets/96921261/5df89c13-7c16-4460-8e1c-663c260b0f06)

![FinalIMG](https://github.com/AliAmini93/Electrical-Board-detection/assets/96921261/fe0343b8-4d4a-4263-9646-15f79818a79c)

![93](https://github.com/AliAmini93/Electrical-Board-detection/assets/96921261/10a8fff3-951b-4c2c-87c2-531d2782a742)

![97](https://github.com/AliAmini93/Electrical-Board-detection/assets/96921261/65ddc1ea-4327-4433-ba03-b3ea180c6f2f)

![545](https://github.com/AliAmini93/Electrical-Board-detection/assets/96921261/3f4c0f31-991e-4630-ace5-37c575fba67a)

![val_batch1_pred](https://github.com/AliAmini93/Electrical-Board-detection/assets/96921261/1d495115-1045-42b1-9a52-c81a8e803161)

![val_batch0_pred](https://github.com/AliAmini93/Electrical-Board-detection/assets/96921261/dde8edbb-6434-4cbe-8d77-96c21c546d4a)

![val_batch2_pred](https://github.com/AliAmini93/Electrical-Board-detection/assets/96921261/84c80a2b-4643-4de3-9ac9-77488bd81aa8)

![results](https://github.com/AliAmini93/Electrical-Board-detection/assets/96921261/775b56be-0ecb-407d-83bb-e6f84cc31607)

![confusion_matrix](https://github.com/AliAmini93/Electrical-Board-detection/assets/96921261/f75fdfec-67e9-485b-b96a-32c62fc709c5)
## IC Detection

### 1. Dataset Utilization and Annotation
- **Task**: Employ the same dataset with distinct annotations for IC detection.
- **Details**: The dataset includes 3 types of ICs: without, four-sided, and two-sided ICs.

### 2. Model Selection and Training
- **Task**: Experiment with different YOLO versions for fine-tuning.
- **Process**: Various training configurations and data augmentation techniques were tested.
- **Result**: The best model, based on its performance on the test set, was selected for further analysis.
- **Model Availability**: The fine-tuned model can be provided upon request.

![FinalIMGFinalIMG-IC-Detected](https://github.com/AliAmini93/Automated-Circuit-Analysis-System/assets/96921261/0dc2f522-3b4c-4ed1-b0ce-f5dc2f986136)

![compressed_600](https://github.com/AliAmini93/Automated-Circuit-Analysis-System/assets/96921261/4c8c03d0-f066-43fa-8fa8-f1f74aaccfee)

![compressed_581](https://github.com/AliAmini93/Automated-Circuit-Analysis-System/assets/96921261/686aee60-bdb0-4bbd-9380-5c13bd2987c4)

![599](https://github.com/AliAmini93/Automated-Circuit-Analysis-System/assets/96921261/e5f48554-c944-4545-9c29-3d8e72a676a8)

![1](https://github.com/AliAmini93/Automated-Circuit-Analysis-System/assets/96921261/92b59cd6-b05f-48e3-97fc-70c99ee0a2de)

![PR_curve](https://github.com/AliAmini93/Automated-Circuit-Analysis-System/assets/96921261/c5825eab-91f2-45ae-bac3-fcde7711dd27)

![P_curve](https://github.com/AliAmini93/Automated-Circuit-Analysis-System/assets/96921261/ac866578-af70-4574-b121-40f98e550f27)

![confusion_matrix](https://github.com/AliAmini93/Automated-Circuit-Analysis-System/assets/96921261/6883fd4b-429d-40de-a6d8-fba7b906cdbf)

## IC Recognition

### 1. Box Detection on ICs
- **Task**: Detect boxes containing text on each IC using a fine-tuned YOLO model.
- **Model Details**: The model is specifically trained for the precise detection of text boxes on integrated circuits.
- **Model Availability**: The fine-tuned YOLO model can be provided upon request.

### 2. Text Recognition within Boxes
- **Task**: Recognize the text within each detected box.
- **Method**: Utilize a fine-tuned PaddleOCR for accurate text recognition.
- **Process**: PaddleOCR works in conjunction with the YOLO model to effectively recognize text in the identified areas.
- **Model Availability**: The fine-tuned PaddleOCR model is available upon request.
- **Implementation**: The `ocr.py` script is used for the detection and recognition tasks in this part.

### 3. Logo Detection
- **Task**: Identify company logos on the ICs.
- **Method**: Use a fine-tuned YOLO model trained on a dataset of 20 different company logos.
- **Objective**: Facilitate the process of recognizing each IC by identifying the associated company logo.
- **Model Availability**: The logo detection model is accessible upon request.


