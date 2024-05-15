from flask import Flask, request, render_template
import cv2
import numpy as np
from moviepy.editor import VideoFileClip
import os
import uuid
import io

app = Flask(__name__)

# Classes
classNames = {0: 'background',
              8: 'cat'
              }

# ssd
prototype = "SSD_using_OpenCV/MobileNetSSD_deploy.prototxt"
weights = "SSD_using_OpenCV/MobileNetSSD_deploy.caffemodel"
net = cv2.dnn.readNetFromCaffe(prototype, weights)

# for img
def process_image(img):
    img_resize = cv2.resize(img, (300, 300))
    blob = cv2.dnn.blobFromImage(img_resize, 0.007843, (300, 300),
                                 (127.5, 127.5, 127.5), False)
    net.setInput(blob)
    detections = net.forward()

    height, width, _ = img.shape

    final = detections.squeeze()

    font = cv2.FONT_HERSHEY_SIMPLEX

    processed_image = img.copy()

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

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename != '':
            if file.filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                img_bytes = file.read()
                nparr = np.frombuffer(img_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                processed_img = process_image(img)
                if processed_img is not None:
                    output_filename = f"processed_image_{uuid.uuid4()}.jpg"
                    cv2.imwrite(output_filename, processed_img)
                    return render_template('result.html', filename=output_filename)
                else:
                    return "Unsupported file format"
            elif file.filename.endswith(('.mp4')):
                video_bytes = file.read()
                video_stream = io.BytesIO(video_bytes)
                clip = VideoFileClip(video_stream)
                out_folder = 'static/img/uploads/processed'
                out_filename = f'processed_video_{uuid.uuid4()}.mp4'
                out_path = os.path.join(out_folder, out_filename)
                processed_clip = clip.fl_image(process_image)
                processed_clip.write_videofile(out_path, audio=True)
                return render_template('result.html', filename=out_filename)
            else:
                return "Unsupported file format"
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
