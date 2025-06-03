from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

def get_predictions(text):
    if not text.strip():
        return []

    inputs = tokenizer.encode(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=inputs.shape[1] + 5,
            num_return_sequences=1,
            do_sample=True,
            top_k=50,
            temperature=0.8
        )

    generated = tokenizer.decode(outputs[0])
    suffix = generated[len(text):].strip()
    return suffix.split()[:3] if suffix else []
