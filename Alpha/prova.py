#
import pandas as pd
#
# df_dirty = pd.read_csv("TechBuyer_DMA_-_Experience_Assessment_-_Final.xlsx - Questions.csv")
#
# df = df_dirty[["Key Success Stage", "Key Success Area", "Description"]]
#
# question_dict = {}
#
# ksss = df["Key Success Stage"].unique()
# for kss in ksss:
#     ksas = df["Key Success Area"].where(df["kss"] == kss).dropna().unique()
#     ksa_dict = {}
#     for ksa in ksas:
#         questions = df["Description"].where(df["Key Success Area"] == ksa).dropna()
#         question_list = []
#         for q in questions:
#             question_list.append(q)
#         ksa_dict[ksa] = question_list
#         question_dict[kss] = ksa_dict
#
# df.to_csv("questions.csv")

df = pd.read_csv("Priority_Table.csv")
print(df.head(5))