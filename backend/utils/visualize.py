import cv2

def draw_boxes(image_path, boxes):

    image = cv2.imread(image_path)

    for box in boxes:
        x0, y0, x1, y1 = box
        cv2.rectangle(image, (x0, y0), (x1, y1), (0,255,0), 2)

    return image