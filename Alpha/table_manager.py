import pandas as pd
import database_manager as dm
from questions import ksas_points, questions_points, efforts

df = pd.DataFrame(
    columns=["KSS", "KSA", "Description", "KSA Points", "Question Points", "CSR", "Weight", "Active W", "Exclude",
             "Effort", "Forecast", "Priority"])

with dm.app.app_context():
    df["KSS"] = [kss[0] for kss in dm.db.session.query(dm.Question.kss).all()]  # creo la lista di kss dal database

with dm.app.app_context():
    df["KSA"] = [ksa[0] for ksa in dm.db.session.query(dm.Question.ksa).all()]

with dm.app.app_context():
    df["Description"] = [description[0] for description in dm.db.session.query(dm.Question.description).all()]

df["KSA Points"] = ksas_points()  # Questa lista andrà ricavata dai risultati dell'altro survey che identifica il tipo di azienda

df["CSR"] = dm.user_results(3)

df["Question Points"] = questions_points()  # Questa lista andrà ricavata dai risultati dell'altro survey che identifica il tipo di azienda

weight_list = []
for index, row in df.iterrows():  # scorro ogni riga del dataframe
    ksa = row["KSA"]
    ksa_total_qp = df.groupby("KSA")["Question Points"].sum()[ksa]  # faccio la somma dei question points totali del ksa
    weight_list.append(round((row["Question Points"] / ksa_total_qp), 3))  # appendo la % di pesa che ha la domanda rispetto al valore tot calcolato sopra
df["Weight"] = weight_list

active_w_list = []
for index, row in df.iterrows():
    weight = row["Weight"]
    csr = row["CSR"]
    active_w_list.append(round(weight * (csr / 5), 3))  # calcolo quanto peso realmente ha la domanda sul ksa
df["Active W"] = active_w_list

df["Exclude"] = False

df["Effort"] = efforts()  # per ora lo otteniamo così ma da valutare come inserirlo

priority_list = []
for index, row in df.iterrows():
    weight = row["Weight"]
    active_w = row["Active W"]
    ksa_points = row["KSA Points"]
    effort = row["Effort"]
    if row["Exclude"] == False:
        priority_list.append(round(((weight - active_w) * ksa_points) / effort, 2))
    else:
        priority_list.append(0)

df["Priority"] = priority_list

pd.set_option('display.max_columns', None)  # per visualizzare tutte le colonne, ma solo qua per dimostrazione
print(df.head())

df.to_csv("Priority_Table.csv", index=False)

# pd.set_option('display.max_columns', None)
# print(df.KSA.value_counts()["Taxonomy"])  # con questo comando riesco a vedere quante domande corrispondono a Taxonomy

