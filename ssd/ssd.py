import numpy as np
import cv2

# Classes
classNames = {0: 'background',
              8: 'cat',
              12: 'dog'}

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
            image = cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 3)
            image = cv2.putText(image, class_name, (int(x1), int(y1) - 10), font,
                                1, (255, 0, 0), 2, cv2.LINE_AA)
    return image


input_path = "/home/chudishe/PycharmProjects/pythonProject/photo_2024-04-26_18-33-50.jpg"
if input_path.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
    # if img
    img = cv2.imread(input_path)
    processed_img = process_image(img)
    cv2.imshow("Image", processed_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    # if mp4
    cap = cv2.VideoCapture(input_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        processed_frame = process_image(frame)
        cv2.imshow("Video", processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
