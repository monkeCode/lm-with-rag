from typing import Any, Generator
import model_interface
from huggingface_hub import InferenceClient
import os.path

CONFIG_FILE = "settings.conf"

if (os.path.isfile(CONFIG_FILE)):
    with open(CONFIG_FILE, mode="r") as f:
        token = f.readline()
else:
    raise FileNotFoundError("config file does not exist")

class Phi3(model_interface.Model):
    def __init__(self):
        self.client = InferenceClient(api_key=token)

    def generate_text(self, messages) -> Generator[str | None, Any, None]:
        stream = self.client.chat.completions.create(
                model="microsoft/Phi-3.5-mini-instruct", 
                messages=messages, 
                max_tokens=1024,
                stream=True,
                temperature=0.3
            )
        for chunk in stream:
            yield chunk.choices[0].delta.content
        


if __name__ == "__main__":
    model = Phi3()
    messages = [ {"role": "system", "content": 
            "you are an helpful assistant"}, ] 

    while(True):
        messages.append( {"role": "user", "content": input()})
        msg = ""
        for chunk in model.generate_text(messages):
            msg += chunk
            print(chunk, end="")
        print()
        
        messages.append({"role":"assistant", "content": msg})