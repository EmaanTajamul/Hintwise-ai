
import torch
from model_loader import load_model


def test_math_hint_tutor():
    print("\nLoading our fine-tuned Math Hint Tutor...")

    # Load Qwen base model + our trained LoRA adapter
    tokenizer, model = load_model()

    # Test question
    question = (
        "Ali has 5 apples. He buys 3 more apples. "
        "How many apples does he have now?"
    )

    # Prepare conversation
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful math tutor. "
                "Give the student one short and useful hint. "
                "Do not reveal the final answer. "
                "Guide the student step by step."
            )
        },
        {
            "role": "user",
            "content": f"Math problem: {question}"
        }
    ]

    print("\nGenerating hint...")

    # Convert conversation into model input
    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
        return_dict=True
    )

    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    # Generate response
    with torch.inference_mode():
        outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=100,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

    # Extract newly generated tokens only
    new_tokens = outputs[0][input_ids.shape[-1]:]

    # Decode model response
    hint = tokenizer.decode(
        new_tokens,
        skip_special_tokens=True
    ).strip()

    # Display results
    print("\n" + "=" * 50)
    print("       MATH HINT TUTOR - TEST RESULT")
    print("=" * 50)

    print("\nStudent's Question:")
    print(question)

    print("\nFine-tuned Model's Hint:")
    print(hint if hint else "No response generated.")

    print("\n" + "=" * 50)
    print("Test completed.")
    print("=" * 50)


if __name__ == "__main__":
    test_math_hint_tutor()

