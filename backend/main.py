
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import torch
from fastapi.middleware.cors import CORSMiddleware

from backend.model_loader import load_model

app = FastAPI(
    title="Math Hint Tutor API",
    description="Fine-tuned AI Math Hint Generation",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load our fine-tuned model once when the API starts
tokenizer = None
model = None


@app.on_event("startup")
def startup_event():
    global tokenizer, model
    print("Loading Fine-tuned Math Hint Tutor...")
    tokenizer, model = load_model()
    print("Math Hint Tutor API is ready!")


class HintRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=2000)


@app.get("/")
def home():
    return {
        "message": "Welcome to Math Hint Tutor API",
        "status": "Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


@app.post("/generate-hint")
def generate_hint(request: HintRequest):

    if model is None or tokenizer is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not loaded yet."
        )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful math tutor. "
                "Give one short and useful hint. "
                "Do not reveal the final answer. "
                "Guide the student toward solving the problem."
            )
        },
        {
            "role": "user",
            "content": f"Math problem: {request.question}"
        }
    ]

    try:
        inputs = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
            return_dict=True
        )

        with torch.inference_mode():
            outputs = model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_new_tokens=100,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id
            )

        new_tokens = outputs[0][inputs["input_ids"].shape[-1]:]

        hint = tokenizer.decode(
            new_tokens,
            skip_special_tokens=True
        ).strip()

        return {
            "question": request.question,
            "hint": hint,
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Hint generation failed: {str(e)}"
        )

