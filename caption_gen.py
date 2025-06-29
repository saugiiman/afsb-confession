from transformers import pipeline
import random

# Load the GPT-2 model
captioner = pipeline("text-generation", model="gpt2")

# List of Gen Z-style emojis to sprinkle randomly
emojis = ["😂", "💀", "🔥", "😳", "🤐", "😶‍🌫️", "👀", "💘", "☠️", "😩", "🙈", "🧍", "😮‍💨", "🫣", "📩", "🧃", "🫡"]

def generate_caption(confession_text):
    # Prepare prompt for AI
    prompt = f"Write a Gen Z Instagram caption for this confession:\n\"{confession_text}\"\nCaption:"

    try:
        # Generate base caption using GPT-2
        result = captioner(prompt, max_length=50, num_return_sequences=1)
        raw_caption = result[0]['generated_text'].split("Caption:")[-1].strip()

        # Clean up and limit length
        caption = raw_caption.replace("\n", " ").strip()
        if len(caption) > 120:
            caption = caption[:115] + "..."

    except Exception:
        # Fallback in case GPT fails
        caption = "Anonymous said it, and we just posted it 😶‍🌫️"

    # Add 2 random emojis at end (can increase if you like)
    final_caption = f"{caption} {random.choice(emojis)} {random.choice(emojis)}"
    return final_caption
