from PIL import Image
import torch
from transformers import AutoProcessor, LayoutLMv3Model

processor = AutoProcessor.from_pretrained(
    "microsoft/layoutlmv3-base",
    apply_ocr=False
)

model = LayoutLMv3Model.from_pretrained(
    "microsoft/layoutlmv3-base"
)

def normalize_box(box, width, height):
    x0, y0, x1, y1 = box

    return [
        int(1000 * x0 / width),
        int(1000 * y0 / height),
        int(1000 * x1 / width),
        int(1000 * y1 / height),
    ]


def get_document_embeddings(image_path, words, boxes):

    image = Image.open(image_path).convert("RGB")

    width, height = image.size

    normalized_boxes = [
        normalize_box(box, width, height)
        for box in boxes
    ]

    encoding = processor(
        image,
        words,
        boxes=normalized_boxes,
        return_tensors="pt",
        truncation=True,
        padding="max_length"
    )

    with torch.no_grad():
        outputs = model(**encoding)

    return outputs.last_hidden_state