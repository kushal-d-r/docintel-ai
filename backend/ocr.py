import easyocr

reader = easyocr.Reader(['en'])

def extract_text_with_boxes(image_path):

    results = reader.readtext(image_path)

    words = []
    boxes = []

    for result in results:
        box, text, confidence = result

        words.append(text)

        x0 = int(box[0][0])
        y0 = int(box[0][1])
        x1 = int(box[2][0])
        y1 = int(box[2][1])

        boxes.append([x0, y0, x1, y1])

    return words, boxes