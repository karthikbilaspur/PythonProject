# echo_scribe.py - Minimalist Infinite Story
import torch
from collections import deque
from transformers import T5ForConditionalGeneration, T5Tokenizer

class EchoScribe:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = T5Tokenizer.from_pretrained('t5-base')
        self.model = T5ForConditionalGeneration.from_pretrained('t5-base').to(self.device)
        self.memory = deque(maxlen=5) # last 5 story chunks

    def write(self, prompt: str) -> str:
        context = " ".join(self.memory) + f" {prompt}" if self.memory else prompt
        ids = self.tokenizer.encode(f"continue story: {context}", return_tensors="pt", truncation=True, max_length=512).to(self.device)
        out = self.model.generate(ids, max_length=320, do_sample=True, temperature=0.9, top_p=0.95, repetition_penalty=1.1)
        story = self.tokenizer.decode(out[0], skip_special_tokens=True)
        self.memory.append(story)
        return story

def main():
    scribe = EchoScribe()
    print("Echo Scribe v2 - Type 'quit' to exit, 'reset' to clear memory, 'history' to see context")
    while True:
        p = input("\n> ").strip()
        if not p: continue
        if p == "quit": break
        if p == "reset":
            scribe.memory.clear()
            print("Memory cleared.")
            continue
        if p == "history":
            print("\n".join(scribe.memory))
            continue

        result = scribe.write(p)
        print(f"\n{result}")

if __name__ == "__main__":
    main()