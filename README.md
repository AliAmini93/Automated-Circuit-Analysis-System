# Automated Circuit Analysis System
This multifaceted project is comprised of 5 main sections including 2D Image Representation, Electrical Board Detection, IC detection, IC Recognition, and preparing a GUI to automate the entire process.
## 2D Image Representation

### 1. Data Collection
- **Task**: Capture images using a provided platform, ensuring significant overlap for accuracy.

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
