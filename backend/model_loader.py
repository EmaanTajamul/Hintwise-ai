
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Original base model
BASE_MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"

# Project adapter path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = PROJECT_ROOT / "model" / "math_tutor_adapter"

def load_model():
    print("Loading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID)

    print("Loading Qwen base model on CPU...")

    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_ID,
        torch_dtype="auto",
        low_cpu_mem_usage=True
    )

    print("Attaching our trained LoRA adapter...")

    model = PeftModel.from_pretrained(
        base_model,
        str(ADAPTER_PATH),
        is_trainable=False
    )

    model.eval()

    print("Our fine-tuned Math Hint Tutor is ready!")

    return tokenizer, model


if __name__ == "__main__":
    tokenizer, model = load_model()
    print("Model loaded successfully.")
