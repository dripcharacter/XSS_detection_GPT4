import pandas as pd

result_df=pd.read_csv("./gpt4_turbo_GPT_XSS_Answer.csv")
answer_df=pd.read_csv("./gpt4_turbo_processed_XSS_dataset.csv")

tp=0
fp=0
tn=0
fn=0
fplist=list()
fnlist=list()

for (idx, result) in enumerate(result_df['GPT_Detection']):
    if result==True:
        if answer_df['Label'][idx]==1:
            tp+=1
        else:
            fp+=1
            fplist.append((result_df['GPT_Input'][idx], result_df['GPT_CoT'][idx], result_df['GPT_Vuln'][idx], result_df['GPT_Detection'][idx]))
    else:
        if answer_df['Label'][idx]==0:
            tn+=1
        else:
            fn+=1
            fnlist.append((result_df['GPT_Input'][idx], result_df['GPT_CoT'][idx], result_df['GPT_Vuln'][idx], result_df['GPT_Detection'][idx]))

print(f"tp, fp, tn, fn = {tp}, {fp}, {tn}, {fn}")
print("===============================================")
print(fplist)
print("===============================================")
print(fnlist)