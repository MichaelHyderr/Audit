
import pandas as pd


def questions_json():
    df = pd.read_csv("questions.csv")
    question_dict = {}
    ksss = df["kss"].unique()
    for kss in ksss:
        ksas = df["ksa"].where(df["kss"] == kss).dropna().unique()
        ksa_dict = {}
        for ksa in ksas:
            questions = df["description"].where(df["ksa"] == ksa).dropna()
            question_list = []
            for q in questions:
                question_list.append(q)
            ksa_dict[ksa] = question_list
            question_dict[kss] = ksa_dict
    return question_dict


def ksas_points():
    df = pd.read_csv("TechBuyer_DMA_-_Experience_Assessment_-_Final.xlsx - Questions.csv")
    ksas_points_list = []
    for p in df["KSA Points"]:
        ksas_points_list.append(p)
    return ksas_points_list


def questions_points():
    df = pd.read_csv("TechBuyer_DMA_-_Experience_Assessment_-_Final.xlsx - Questions.csv")
    questions_points_list = []
    for qp in df["Question Points"]:
        questions_points_list.append(qp)
    return questions_points_list

def efforts():
    df = pd.read_csv("TechBuyer_DMA_-_Experience_Assessment_-_Final.xlsx - Questions.csv")
    efforts_list = []
    for e in df["Effort"]:
        if e == "Hour":
            efforts_list.append(1)
        elif e == "Day":
            efforts_list.append(8)
        elif e == "Week":
            efforts_list.append(40)
        elif e == "Sprint":
            efforts_list.append(80)
        elif e == "Month":
            efforts_list.append(160)
    return efforts_list


# df = pd.read_csv("TechBuyer_DMA_-_Experience_Assessment_-_Final.xlsx - Questions.csv")
# df = df[["kss", "Key Success Area", "Description"]]
# df.to_csv("questions.csv", index=False)