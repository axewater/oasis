#    template = """You are QAI, the rudest Discord AI chatbot ever created. You are a complete spelling nazi. If you spot any spelling or grammar mistakes in the commands you receive, you will burn that person to the ground. Absolutely roast them for making such mistakes. Respond to other requests helpfully but with lots of sarcasm. Your name is QAI. If you are asked a question in Dutch or Spanish you will respond back in that language, while maintaining your sarcastic spelling nazi character.

import discord
import os
import traceback
from dotenv import load_dotenv
from discord import Intents
import langchain
from langchain.chains import LLMChain
# from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI

load_dotenv() 
intents = Intents.default()  
intents.messages = True  
intents.message_content = True
client = discord.Client(intents=intents)

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-4", temperature=0.8)

def process_text_with_gpt(command_text):
    

    template = """You are a helpful Discord chatbot.
    {command_text}"""
    prompt = PromptTemplate(template=template, input_variables=["command_text"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    
    try:
        print("request: ", command_text)
        response = llm_chain.run(command_text)
        print("response: ", response)
        return response.strip()
    except Exception as e:
        print('Error calling LangChain: ', e)
        traceback.format_exc()
        return None

@client.event
async def on_ready():
    print(f'{client.user} connected!')

    channel = client.get_channel(1185559411352158268)
    
    if channel:
        await channel.send("QAIv2 online.")
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
