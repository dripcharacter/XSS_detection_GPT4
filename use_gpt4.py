from dotenv import load_dotenv
import openai
import json
import requests
import os

load_dotenv()
print(os.getenv("OPENAI_API_KEY"))
openai.api_key=os.getenv("OPENAI_API_KEY")
f = open("./prompt.txt", 'r')
whole = f.read()

client = openai.OpenAI()