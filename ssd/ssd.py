import cv2
import numpy as np
from moviepy.editor import VideoFileClip
import os
import uuid

# Classes
classNames = {0: 'background',
              8: 'cat'
              }

# ssd
prototype = "SSD_using_OpenCV/MobileNetSSD_deploy.prototxt"
weights = "SSD_using_OpenCV/MobileNetSSD_deploy.caffemodel"
net = cv2.dnn.readNetFromCaffe(prototype, weights)


# for img
def process_image(image):
    img_resize = cv2.resize(image, (300, 300))
    blob = cv2.dnn.blobFromImage(img_resize, 0.007843, (300, 300),
                                 (127.5, 127.5, 127.5), False)
    net.setInput(blob)
    detections = net.forward()

    height, width, _ = image.shape

    final = detections.squeeze()

    font = cv2.FONT_HERSHEY_SIMPLEX

    processed_image = image.copy()  # Create a copy of the image to modify

    for i in range(final.shape[0]):
        conf = final[i, 2]
        class_id = int(final[i, 1])
        if class_id in classNames and conf > 0.5:
            class_name = classNames[class_id]
            x1, y1, x2, y2 = final[i, 3:]
            x1 *= width
            y1 *= height
            x2 *= width
            y2 *= height
            top_left = (int(x1), int(y1))
            bottom_right = (int(x2), int(y2))
            processed_image = cv2.rectangle(processed_image, top_left, bottom_right, (0, 255, 0), 3)
            processed_image = cv2.putText(processed_image, class_name, (int(x1), int(y1) - 10), font,
                                          1, (255, 0, 0), 2, cv2.LINE_AA)
    return processed_image


input_path = "/home/chudishe/PycharmProjects/pythonProject/src/videoplayback.mp4"

if input_path.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
    # if img
    img = cv2.imread(input_path)
    processed_img = process_image(img)
    cv2.imshow("Image", processed_img)
    output_filename = f"processed_image_{uuid.uuid4()}.jpg"  # Generating random name for the output image file
    cv2.imwrite(output_filename, processed_img)  # Saving the processed image
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    # if mp4
    clip = VideoFileClip(input_path)
    out_path = f'processed_video_{uuid.uuid4()}.mp4'  # Generate a random name for the output video file
    processed_clip = clip.fl_image(process_image)  # Apply the process_image function to each frame
    processed_clip.write_videofile(out_path, audio=True)  # Write the processed clip with audio
