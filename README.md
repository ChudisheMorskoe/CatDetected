# Cat Detection Project

## Overview
The Cat Detection Project is a Python-based application designed to detect cats in both images and videos. It utilizes computer vision techniques to identify and outline the presence of cats within the provided media files. This project is particularly useful for tasks such as pet monitoring, animal welfare, and content moderation.

## Features
- **Image Detection**: The application can process static images in common formats such as JPEG, PNG, BMP, and MP4.
- **Video Detection**: It can also analyze video files, identifying cats in each frame of the footage.
- **Real-Time Processing**: The system provides real-time processing capabilities, enabling users to monitor live video streams for cat detection.
- **User Authentication**: To access the detection functionalities, users must register an account and log in securely.

## Installation
To set up the Cat Detection Project locally, follow these steps:
1. Clone the repository from GitHub: `git clone https://github.com/ChudisheMorskoe/CatDetected.git`
2. Navigate to the project directory: `cd CatDetected`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Run the application: `python app.py`


## Usage
1. **Register/Login**: If you're a new user, sign up for an account. Otherwise, log in using your credentials.
2. **Upload Media**: Choose an image or video file containing cats for analysis.
3. **Detection**: After uploading the file, the application will process it to detect any cats present.
4. **View Results**: Once the analysis is complete, view the results, including any detected cats outlined in the media file.
5. **Download**: Optionally, download the processed media with cat annotations for further use.

## Implementation Details
The Cat Detection Project is built using Python and various libraries, including:
- Flask: For developing the web application and handling HTTP requests.
- OpenCV (cv2): Utilized for image and video processing, including cat detection.
- NumPy: Used for numerical computations and array manipulations.
- MoviePy: Enables the extraction and manipulation of video files.
- SQLite3: Employed for user authentication and database management.
- Werkzeug: Provides utilities for password hashing and secure file handling.

The core cat detection functionality is implemented using the Single Shot MultiBox Detector (SSD) algorithm, which is capable of accurately identifying objects within images and videos.

## Design Considerations
- **User Experience**: The web interface is designed to be intuitive and user-friendly, allowing users to easily upload media files and view detection results.
- **Performance**: Efforts have been made to optimize the detection process for both speed and accuracy, ensuring efficient processing of large image and video datasets.
- **Scalability**: The application architecture is designed to accommodate potential future enhancements, such as support for additional animal species or integration with external APIs.

## Contributions
Contributions to the Cat Detection Project are welcome! If you have suggestions for improvements, bug fixes, or new features, please feel free to submit a pull request on GitHub.

