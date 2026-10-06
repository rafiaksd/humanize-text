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

    "max_tokens": 2048,

    # Enable streaming
    "stream": True
}

request = urllib.request.Request(
    URL,
    data=json.dumps(body).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

print("Generating...\n")

chunks = []

with urllib.request.urlopen(request, timeout=900) as response:
    for line in response:
        line = line.decode("utf-8").strip()

        if not line.startswith("data:"):
            continue

        data = line[5:].strip()

        if data == "[DONE]":
            break

        try:
            chunk = json.loads(data)
            text = chunk["choices"][0].get("text", "")

            if text:
                print(text, end="", flush=True)
                chunks.append(text)

        except json.JSONDecodeError:
            continue

humanized = "".join(chunks).strip()

# Save output
with open("my_script_humanized.txt", "w", encoding="utf-8") as f:
    f.write(humanized)

print("\n\nSaved as: my_script_humanized.txt")
