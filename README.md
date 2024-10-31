                                             Image Studio :
Image Studio is a web-based image editing application built with Flask and OpenCV. Users can upload images and apply various edits such as grayscale conversion, rotation, resizing, cropping, blurring, and edge detection.

image-studio/
├── app.py                  # Main application file
├── static/
│   ├── uploads/            # Folder to store uploaded images
│   └── edited/             # Folder to store edited images
└── templates/
    ├── index.html          # Home page template
    └── edit.html           # Edit page template


Features
Upload Image: Upload an image from your device.
Edit Options:
Convert to grayscale
Rotate to any angle
Resize to custom dimensions
Crop to a specified area
Apply Gaussian blur
Edge detection
Preview edited images and download them in various formats.
Color Info: Hover over the uploaded image to see RGB color values at each point.
