import os
from openai import OpenAI
import gradio as gr
from dotenv import load_dotenv

# Load .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI client
client = OpenAI(api_key=api_key)

# System prompt
system_prompt = os.getenv("PROMPT")

# Chat + voice handler


def juthy_chatbot(prompt):
    # Get text from ChatGPT
    chat_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )
    reply = chat_response.choices[0].message.content

    # Convert reply to audio using OpenAI TTS
    speech_response = client.audio.speech.create(
        model="tts-1",
        voice="nova",  # Options: nova, shimmer, alloy, echo, etc.
        input=reply
    )
    speech_response.stream_to_file("response.mp3")

    return reply, "response.mp3"


# Gradio UI
gr.Interface(
    fn=juthy_chatbot,
    inputs=gr.Textbox(lines=2, placeholder="Ask me something..."),
    outputs=[gr.Textbox(), gr.Audio(type="filepath")],
    title="Hi, I'm Juthy!",
    description="Ask me about my life story, goals, strengths, and learning mindset.",
    allow_flagging="never"
).launch()
