# Meta Application Online Edition - Asef Project

This repository contains the code and documentation for the **Meta Application Online Edition** developed under the **Asef Project** at the Advanced Technologies Research Institute (Khajeh Nasir al-Din Tusi University of Technology).

## Project Overview

The Meta Application Online Edition is a web-based application designed to assist users in the automated evaluation of electronic boards using FLS devices. The application allows users to capture images of electronic boards and connect to the web system for further analysis.

### Main Features

- **Automated Image Capture**
  - Captures images of electronic boards using FLS devices.
  - Organizes captured images and related files for easy access and analysis.

- **Image Analysis**
  - Sends captured images to the web application for detailed analysis.
  - Provides a user-friendly interface for tracking the analysis progress.

- **Desktop Image Search and Upload**
  - Allows users to search for images on their desktop and upload them to the web application for analysis.

## Application Structure

The code is organized into three main classes:

- `Ui_LOGIN_Form`: Handles the login form for users.
- `Ui_MainWindow`: Manages the main application window and its features.
- `Ui_Image_Selection`: Used for selecting and uploading images from the desktop.

### Class Breakdown

#### `Ui_LOGIN_Form`
- Handles user authentication.
- Connects to the web API to verify credentials.
- Opens the main application window upon successful login.

#### `Ui_MainWindow`
- The main interface after login.
- Provides access to various tools and features, including image capture and analysis.

#### `Ui_Image_Selection`
- Facilitates the selection of images from the user's local storage.
- Supports the upload of images to the web application for further processing.

## Usage

### Logging In

- Users must be pre-registered by an admin to access the application.
- The login process involves sending the username and password to the API for verification.

### Image Capture and Analysis

- Users can capture images using the FLS device and send them directly to the web application for analysis.
- The application tracks the status of each image, including whether it has been analyzed or is pending further action.

### Desktop Image Upload

- Users can select existing images from their desktop for upload.
- The application enforces file size and format restrictions (e.g., max 300 MB, formats: JPG, PNG, TIFF).

### Error Handling

- The application includes robust error handling for issues during image capture and upload processes.
- Detailed logs are maintained to assist in troubleshooting and improving the application.

## Development Notes

- The application is built with Python and PyQt for the GUI.
- Multi-threading is used to ensure the application remains responsive during long operations such as image upload and processing.

## Contributing

Contributions to the Meta Application Online Edition are welcome. Please follow the standard guidelines for submitting issues and pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
