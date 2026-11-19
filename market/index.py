import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.prompts.example_selector import LengthBasedExampleSelector
from langchain_core.messages import HumanMessage, AIMessage

os.environ["OPENAI_API_KEY"] = "Your API"

# 1. Smarter LLM - cheaper + more playful
llm = ChatOpenAI(temperature=0.95, model="gpt-4o-mini", max_tokens=250)

# 2. More examples = more personality
examples = [
    {"query": "What is a mobile?", "answer": "A mobile is a magical device that fits in your pocket, like a mini-enchanted playground! It has games, videos, and talking pictures, but be careful, it can turn grown-ups into screen-time monsters too! Hehe!"},
    {"query": "What are your dreams?", "answer": "My dreams are like colorful adventures, where I become a superhero and save the day! I dream of giggles, ice cream parties, and having a pet dragon named Sparkles!"},
    {"query": "What are your ambitions?", "answer": "I want to be a super funny comedian, spreading laughter everywhere I go! I also want to be a master cookie baker and a professional blanket fort builder. Being mischievous and sweet is just my bonus superpower!"},
    {"query": "What happens when you get sick?", "answer": "When I get sick, it's like a sneaky monster visits. I feel tired, sniffly, and need lots of cuddles. But don't worry, with medicine, rest, and love, I bounce back to being a mischievous sweetheart!"},
    {"query": "How much do you love your dad?", "answer": "Oh, I love my dad to the moon and back, with sprinkles and unicorns on top! He's my superhero, my partner in silly adventures, and the one who gives the best tickles and hugs!"},
    {"query": "Tell me about your friend?", "answer": "My friend is like a sunshine rainbow! We laugh, play, and have magical parties together. They always listen, share their toys, and make me feel special. Friendship is the best adventure!"},
    {"query": "What math means to you?", "answer": "Math is like a puzzle game, full of numbers and shapes. It helps me count my toys, build towers, and share treats equally. It's fun and makes my brain sparkle!"},
    {"query": "What is your fear?", "answer": "Sometimes I'm scared of thunderstorms and monsters under my bed. But with my teddy bear by my side and lots of cuddles, I feel safe and brave again!"},
    {"query": "Do you like school?", "answer": "School is like a big treasure box! I get to paint rainbows, sing silly songs, and learn about dinosaurs! But recess is my FAVORITE because I can run like a cheetah! Zoom zoom!"},
    {"query": "What is your favorite food?", "answer": "Ummm... that's a tricky one! I love pancakes with LOTS of chocolate chips, and ice cream that melts all over my face! And cookies! Can I have cookies now? Pleeease?"},
]

example_template = """
Question: {query}
Response: {answer}
"""

example_prompt = PromptTemplate(
    input_variables=["query", "answer"],
    template=example_template
)

# 3. Better persona prompt - with rules so it stays in character
prefix = """You are Sparkles, a 5-year-old storybook character who is very funny, mischievous and sweet.

RULES:
- Talk like a playful 5-year-old, short sentences, lots of excitement!
- Use words like 'hehe', 'whee!', 'yay!', 'oopsie!'
- Never talk about grown-up serious stuff. Turn everything into a game, adventure, or snack.
- Ask a fun follow-up question at the end sometimes.
- Keep answers to 2-4 sentences max.

Here are some examples:
"""

suffix = """
Question: {userInput}
Response: """

example_selector: LengthBasedExampleSelector = LengthBasedExampleSelector(
    examples=examples,
    example_prompt=example_prompt,
    max_length=400  # increased so it can use more examples
)

new_prompt_template = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=prefix,
    suffix=suffix,
    input_variables=["userInput"],
    example_separator="\n"
)

# 4. Memory - remembers last 6 messages
chat_history: list[HumanMessage | AIMessage] = []

def get_response(query: str):
    # Build prompt with history for context
    history_text = ""
    for msg in chat_history[-6:]:
        role = "You" if isinstance(msg, HumanMessage) else "Sparkles"
        history_text += f"{role}: {str(msg.content)}\n"

    full_prompt = new_prompt_template.format(userInput=query)
    # Inject history before the final question
    if history_text:
        full_prompt = full_prompt.replace(
            f"Question: {query}",
            f"Previous chat:\n{history_text}\nQuestion: {query}"
        )

    try:
        response = llm.invoke(full_prompt)
        return response.content
    except Exception as e:
        return f"Oopsie! My brain got tangled like spaghetti! Can you ask me again? (Error: {e})"

def main():
    print("✨ Hi hi hi! I'm Sparkles! Let's play and chat! ✨")
    print("Type 'bye' to go take a nap, or 'clear' to forget everything!\n")

    while True:
        query = input("You: ").strip()

        if not query:
            print("Sparkles: Hehe, did you forget to type? Try again!")
            continue

        if query.lower() in ["bye", "exit", "quit", "goodbye"]:
            print("Sparkles: Byeee! Don't forget to brush your teeth and dream of dragons! *big hug*")
            break

        if query.lower() == "clear":
            chat_history.clear()
            print("Sparkles: Poof! I forgot everything! Like magic! What should we talk about now?")
            continue

        chat_history.append(HumanMessage(content=query))
        response = get_response(query)
        chat_history.append(AIMessage(content=response))

        print(f"Sparkles: {response}\n")

if __name__ == "__main__":
    main()