from transformers import AutoProcessor
from transformers import AutoModelForTokenClassification

processor = AutoProcessor.from_pretrained(
    "microsoft/layoutlmv3-base"
)

model = AutoModelForTokenClassification.from_pretrained(
    "microsoft/layoutlmv3-base"
)