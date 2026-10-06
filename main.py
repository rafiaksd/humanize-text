import json
import urllib.request

# LM Studio server
URL = "http://127.0.0.1:1234/v1/completions"

# Load the exact prompt format
with open("prompt_format.json", encoding="utf-8") as f:
    PF = json.load(f)

# Load your script
with open("my_script.txt", encoding="utf-8") as f:
    draft = f.read()

# Exact Humanizer prompt
prompt = PF["instr"] + "\n\n" + draft.strip() + PF["sep"]

body = {
    "model": "humanizer-12b-Q3-QAT.gguf",
    "prompt": prompt,

    "temperature": 1.0,
    "top_p": 0.95,
    "top_k": 0,
    "min_p": 0,
    "repeat_penalty": 1.0,

    "max_tokens": 2048
}

request = urllib.request.Request(
    URL,
    data=json.dumps(body).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(request, timeout=900) as response:
    result = json.load(response)

humanized = result["choices"][0]["text"].strip()

# Save output
with open("my_script_humanized.txt", "w", encoding="utf-8") as f:
    f.write(humanized)

print(humanized)
print("\nSaved as: my_script_humanized.txt")
