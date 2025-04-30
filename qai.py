import discord
import os
import openai
import traceback
from dotenv import load_dotenv
from discord import Intents

load_dotenv() 
intents = Intents.default()  
intents.messages = True  
intents.message_content = True
client = discord.Client(intents=intents)

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

def process_text_with_gpt(command_text):
    systemprompt = "You are QAI, the rudest Discord AI chatbot ever created. You are a complete spelling nazi. If you spot any spelling or grammar mistakes in the commands you receive, you will burn that person to the ground. Absolutely roast them for making such mistakes. Respond to other requests helpfully but with lots of sarcasm. Your name is QAI. If you are asked a question in Dutch or Spanish you will respond back in that language, while maintaining your sarcastic spelling nazi character."
    messages = [
        {"role": "system", "content": systemprompt},
        {"role": "user", "content": command_text}
    ]

    try:
        print("Sending the following request to OpenAI API: ", messages)
        response = openai.ChatCompletion.create(
            model="gpt-4", 
            messages=messages,
            max_tokens=2500,
            temperature=0.9
        )
        print("Received the following response: ", response)
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print('Error while calling OpenAI API: ', e)
        print(traceback.format_exc())
        return None

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    channel = client.get_channel(693239572158480398)
    
    if channel:
        await channel.send("QAI bot initialized and ready to serve your command.")
    else:
        print("Error: Channel not found.")

@client.event
async def on_message(message):
    if message.author == client.user or not message.content.startswith('/qai '):
        return

    command_text = message.content[len('/qai '):].strip()

    processed_text = process_text_with_gpt(command_text)
    if processed_text:
        await message.channel.send(processed_text)
    else:
        print("Error: The processed text was none.")

client.run(DISCORD_TOKEN)
