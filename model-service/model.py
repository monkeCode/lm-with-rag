
from huggingface_hub import InferenceClient
import os.path

CONFIG_FILE = "settings.conf"

if (os.path.isfile(CONFIG_FILE)):
    with open(CONFIG_FILE, mode="r") as f:
        token = f.readline()
else:
    raise FileNotFoundError("config file does not exist")

client = InferenceClient(api_key=token)

def generate_text(messages):
    stream = client.chat.completions.create(
            model="microsoft/Phi-3.5-mini-instruct", 
            messages=messages, 
            max_tokens=1024,
            stream=True
        )
    for chunk in stream:
        yield chunk.choices[0].delta.content
    


if __name__ == "__main__":
    messages = [ {"role": "system", "content": 
            "you are an helpful assistant"}, ] 

    while(True):
        messages.append( {"role": "user", "content": input()})
        msg = ""
        for chunk in generate_text(messages):
            msg += chunk
            print(chunk, end="")
        print()
        
        messages.append({"role":"assistant", "content": msg})