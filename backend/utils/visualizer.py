import cv2
import os


def is_match(word, value):

    if not value:
        return False

    word = str(word).lower().strip()
    value = str(value).lower().strip()

    return word in value or value in word


def get_color(field_name):

    field_name = field_name.lower()

    if "name" in field_name:
        return (0, 255, 0)      # Green

    elif "dob" in field_name:
        return (255, 0, 0)      # Blue

    elif (
        "aadhaar" in field_name
        or "pan" in field_name
        or "passport" in field_name
        or "license" in field_name
        or "epic" in field_name
    ):
        return (0, 0, 255)      # Red

    elif "address" in field_name:
        return (0, 255, 255)    # Yellow

    else:
        return (255, 255, 255)


def draw_boxes(image_path, boxes, words, fields):

    image = cv2.imread(image_path)

    if image is None:
        raise Exception("Image not found.")

    for word, box in zip(words, boxes):

        for field_name, value in fields.items():

            if field_name == "document_type":
                continue

            if is_match(word, value):

                color = get_color(field_name)

                x1, y1, x2, y2 = box

                cv2.rectangle(
                    image,
                    (x1, y1),
                    (x2, y2),
                    color,
                    2
                )

                cv2.putText(
                    image,
                    field_name,
                    (x1, max(20, y1 - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.45,
                    color,
                    1
                )

                break

    output_folder = "outputs/images"

    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(
        output_folder,
        os.path.basename(image_path)
    )

    cv2.imwrite(output_path, image)

    return output_path