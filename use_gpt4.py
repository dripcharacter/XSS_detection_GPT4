from dotenv import load_dotenv
import openai
import json
import os

load_dotenv()
print(os.getenv("OPENAI_API_KEY"))
openai.api_key=os.getenv("OPENAI_API_KEY")
f = open("./prompt.txt", 'r')
whole = f.read()

client = openai.OpenAI()

response=client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "Suppose you are a security expert at XSS detection."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": whole,
                }
            ]
        },
        {
            "role": "assistant",
            "content": "Okay, I will reponse as your instruction"
        },
        {
            "role": "user",
            "content": """<meta name="viewport" content="width=device-width, initial-scale=1.0">"""
        }
    ],
    max_tokens=4096
)
result=response.choices[0].message.content
print(result)
result=json.loads(response.choices[0].message.content.strip("`""json""\n"))
print(result)
print(type(result))
print(result['CoT_Process'])
print(result['Expected_Vulnerabilities'])
print(result['XSS_Detection'])
# {
#     CoT_Process: {
#         Step_1: <your answer about Step 1>,
#         Step_2: <your answer about Step 2>,
#         Step_3: <your answer about Step 3>,
#         Step_4: <your answer about Step 4>
#     },
#     Expected_Vulnerabilities: [<vulnerabilities what you expected through CoT Steps>],
#     XSS_Detection: [<boolean value about XSS_Detection>]
# }