from dotenv import load_dotenv
import openai
import json
import os
import pandas as pd

def use_gpt4(data, model_name):
    load_dotenv()
    openai.api_key=os.getenv("OPENAI_API_KEY")
    f = open("./prompt.txt", 'r')
    whole = f.read()

    client = openai.OpenAI()

    response=client.chat.completions.create(
        model=model_name,
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
                "content": f"""{data}"""
            }
        ],
        max_tokens=4096
    )
    result=response.choices[0].message.content
    result=result.strip("`""json""\n")
    result=json.loads(result)

    return result

df=pd.read_csv('./gpt4_turbo_processed_XSS_dataset.csv')
answer_df=pd.read_csv('./gpt4_turbo_GPT_XSS_Answer.csv')
df=df.iloc[len(answer_df):]

for idx, data in enumerate(df['Sentence'].values):
    print(f"=============================={idx}==================================")
    result=use_gpt4(data)
    print(f"CoT_Process: {result['CoT_Process']}")
    print(f"Vuln: {result['Expected_Vulnerabilities']}")
    print(f"Detection: {result['XSS_Detection']}")
    pd.DataFrame({
        'GPT_Input':[data],
        'GPT_CoT':[result['CoT_Process']],
        'GPT_Vuln':[result['Expected_Vulnerabilities']],
        'GPT_Detection':[result['XSS_Detection']]
    }).to_csv("./gpt4_turbo_GPT_XSS_Answer.csv", mode='a', header=False, index=False)

    
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