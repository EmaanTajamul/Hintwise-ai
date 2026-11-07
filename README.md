# HintWise AI — Math Hint Tutor

**Think Smarter. Solve Step by Step.**

HintWise AI is an AI-powered math tutoring application that helps students solve mathematical word problems through step-by-step hints instead of directly revealing the final answer.

## Project Overview

The project uses a small language model fine-tuned with QLoRA to generate useful next-step hints for math word problems.

Rather than simply providing answers, HintWise AI encourages students to think independently and understand the mathematical operations involved.

## Key Features

- AI-generated hints for math word problems.
- Fine-tuned Qwen2.5-1.5B-Instruct model.
- QLoRA-based parameter-efficient fine-tuning.
- FastAPI backend for hint generation.
- Interactive web frontend.
- Designed to guide students without directly revealing answers.

## Tech Stack

| Component | Technology |
|---|---|
| Base Model | Qwen2.5-1.5B-Instruct |
| Fine-tuning | QLoRA, LoRA, PEFT |
| Backend | Python, FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Model Libraries | Transformers, PyTorch |
| API Testing | Swagger UI |

## How It Works

1. A student enters a mathematical word problem.
2. The frontend sends the question to the FastAPI backend.
3. The backend passes the question to the fine-tuned Qwen model.
4. The model generates a short educational hint.
5. The frontend displays the hint to guide the student.

## Model Fine-Tuning and Evaluation

The model was fine-tuned using QLoRA on a synthetic dataset of 40 math problem-and-hint examples.

Evaluation was conducted on 20 unseen math problems by comparing the original model with the fine-tuned model.

## Supported Math Examples

- Addition
- Subtraction
- Multiplication
- Division

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/hintwise-ai.git
cd hintwise-ai
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the backend

```bash
python -m uvicorn backend.main:app --reload
```

### 5. Open the API documentation

Visit:

`http://127.0.0.1:8000/docs`

### 6. Run the frontend

Open `frontend/index.html` using VS Code Live Server.

The fine-tuned adapter must be available in `model/math_tutor_adapter/`. The base Qwen model is downloaded from Hugging Face when the backend loads it.

## Project Structure

```text
Math_Hint_Tutor/
│
├── backend/
│   ├── main.py
│   ├── model_loader.py
│   └── test_model.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── model/
│   └── math_tutor_adapter/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Project Goal

The goal of HintWise AI is to make math learning more interactive by guiding students toward solutions instead of simply giving them answers.

---

**Developed as an AI/ML fine-tuning project using QLoRA and Qwen2.5.**