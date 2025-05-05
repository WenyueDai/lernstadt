from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # required even if dummy
)

print("Sending prompt...")

response = client.chat.completions.create(
    model="deepseek-r1:7b",
    messages=[{"role": "user", "content": "Was ist der Sinn des Lebens?"}]
)

print("Response received:")
print(response.choices[0].message.content)
