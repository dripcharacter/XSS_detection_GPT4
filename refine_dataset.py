import pandas as pd
import random

result_df=pd.read_csv("./gpt4o_GPT_XSS_Answer.csv")
answer_df=pd.read_csv("./gpt4o_processed_XSS_dataset.csv")

gpt4_turbo_df=pd.read_csv("./gpt4_turbo_processed_XSS_dataset.csv")

tp=0
fp=0
tn=0
fn=0
fplist=list()
fnlist=list()

true_rows = result_df[result_df['GPT_Detection'] == True]
false_rows = result_df[result_df['GPT_Detection'] == False]

for (idx, result) in enumerate(result_df['GPT_Detection']):
    if result==True:
        if answer_df['Label'][idx]==1:
            tp+=1
        else:
            fp+=1
            fplist.append((result_df['GPT_Input'][idx], result_df['GPT_CoT'][idx], result_df['GPT_Vuln'][idx], result_df['GPT_Detection'][idx]))
            pd.DataFrame({
                'Sentence':[result_df['GPT_Input'][idx]],
                'Label':[0],
            }).to_csv("./gpt4_turbo_processed_XSS_dataset.csv", mode='a', header=False, index=False)
            tmp=result_df['GPT_Input'][idx]
            true_rows=true_rows[true_rows['GPT_Input']!=tmp]
    else:
        if answer_df['Label'][idx]==0:
            tn+=1
        else:
            fn+=1
            fnlist.append((result_df['GPT_Input'][idx], result_df['GPT_CoT'][idx], result_df['GPT_Vuln'][idx], result_df['GPT_Detection'][idx]))
            pd.DataFrame({
                'Sentence':[result_df['GPT_Input'][idx]],
                'Label':[1],
            }).to_csv("./gpt4_turbo_processed_XSS_dataset.csv", mode='a', header=False, index=False)
            tmp=result_df['GPT_Input'][idx]
            false_rows=false_rows[false_rows['GPT_Input']!=tmp]



print(f"tp, fp, tn, fn = {tp}, {fp}, {tn}, {fn}")
print("===============================================")
print(fplist)
print("===============================================")
print(fnlist)
true_rows.reset_index(drop=True, inplace=True)
false_rows.reset_index(drop=True, inplace=True)
for _ in range(44):
    true_tmp_idx=random.randint(0, len(true_rows)-1)
    false_tmp_idx=random.randint(0, len(false_rows)-1)
    pd.DataFrame({
        'Sentence':[true_rows['GPT_Input'][true_tmp_idx]],
        'Label':[1],
    }).to_csv("./gpt4_turbo_processed_XSS_dataset.csv", mode='a', header=False, index=False)
    pd.DataFrame({
        'Sentence':[false_rows['GPT_Input'][false_tmp_idx]],
        'Label':[0],
    }).to_csv("./gpt4_turbo_processed_XSS_dataset.csv", mode='a', header=False, index=False)
    true_rows=true_rows[true_rows['GPT_Input']!=true_rows['GPT_Input'][true_tmp_idx]]
    false_rows=false_rows[false_rows['GPT_Input']!=false_rows['GPT_Input'][false_tmp_idx]]
    true_rows.reset_index(drop=True, inplace=True)
    false_rows.reset_index(drop=True, inplace=True)