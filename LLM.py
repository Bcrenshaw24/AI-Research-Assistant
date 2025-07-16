import json
from dotenv import load_dotenv
import os
import requests

def generate(query, corpus):
    load_dotenv() 
    KEY = os.environ.get("GROQ") 
    contexts = [context['metadata']["content"] for context in corpus["matches"]]
    context_str = "\n\n".join(contexts)




    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {KEY}"}
    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": f"You are a helpful assistant, your job is to make topics easily digestible for students. Avoid mentioning the paper itself. Please format every equation in LaTeX, using $...$ for inline equations and $$..$$ for block equations to display cleanly. Do not mention the soruces or texts, even if unrelated, just try to help or ask them to rephrase. Answer '{query}' only using relevant documents from '{context_str}'. "}],
        "temperature": 0.5,
        "max_tokens": 1024, 
        "stream": True
    }
    with requests.post(url, headers=headers, json=data, stream=True) as response:
        response.raise_for_status()
        try:
            for line in response.iter_lines(decode_unicode=True):
                if line and line.startswith("data: "):
                    data_str = line[len("data: "):].strip()
                    if data_str == "[DONE]":
                        break
                    try:
                        data_json = json.loads(data_str)
                        delta = data_json["choices"][0]["delta"].get("content", "")
                        if delta:
                            # ✅ Yield as decoded string with flush newline
                            yield delta
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"Streaming error: {e}")
            yield "\n[Error in streaming]\n"