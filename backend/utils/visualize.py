import cv2
import os


# ---------------------------------------------------
# Check if OCR word belongs to extracted field
# ---------------------------------------------------
def is_match(word: str, value: str):

    if not value:
        return False

    word = word.lower().strip()
    value = value.lower().strip()

    if word in value:
        return True

    if value in word:
        return True

    return False


# ---------------------------------------------------
# Get color for different field types
# ---------------------------------------------------
def get_color(field_name):

    field = field_name.lower()

    if "name" in field:
        return (0, 255, 0)      # Green

    if "dob" in field:
        return (255, 0, 0)      # Blue

    if "gender" in field:
        return (255, 255, 0)    # Cyan

    if (
        "aadhaar" in field
        or "pan" in field
        or "passport" in field
        or "license" in field
        or "epic" in field
    ):
        return (0, 0, 255)      # Red

    if "address" in field:
        return (0, 255, 255)    # Yellow

    return (0, 255, 0)


# ---------------------------------------------------
# Draw ONLY extracted fields
# ---------------------------------------------------
def draw_boxes(image_path, boxes, words, fields):

    image = cv2.imread(image_path)

    if image is None:
        raise Exception("Image not found.")

    for word, box in zip(words, boxes):

        matched = False
        color = (0, 255, 0)

        for field_name, field_value in fields.items():

            if field_name == "document_type":
                continue

            if is_match(word, str(field_value)):

                matched = True
                color = get_color(field_name)
                break

        if not matched:
            continue

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
            word,
            (x1, max(20, y1 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            1
        )

    output_folder = "outputs/images"
    os.makedirs(output_folder, exist_ok=True)

    filename = os.path.basename(image_path)

    output_path = os.path.join(
        output_folder,
        filename
    )

    cv2.imwrite(output_path, image)

    return output_path