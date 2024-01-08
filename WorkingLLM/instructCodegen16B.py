from transformers import AutoModelForCausalLM, AutoTokenizer

checkpoint = "sahil2801/instruct-codegen-16B"
device = "cuda"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint).half().to(device)

instruction = "Write a function to scrape hacker news."
prompt = (f"Below is an instruction that describes a task.\n Write a response that appropriately completes the "
          f"request.\n\n ### Instruction:\n{instruction}\n\n### Response:")
inputs = tokenizer(prompt, return_tensors="pt").to(device)
outputs = model.generate(**inputs, temperature=0.3, do_sample=True, max_new_tokens=256)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
