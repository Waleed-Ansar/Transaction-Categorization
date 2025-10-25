import pickle
import json


with open("Bank Statements.json", "r", encoding="utf-8") as f:
    records = json.load(f)

all_descriptions = []
money = []

for record in records:
    for account in record.get("Accounts", []):
        for transaction in account.get("Transactions", []):
            desc = transaction.get("Description", "")
            mny = transaction.get("WithdrawalAmount") or transaction.get("DepositAmount")
            if desc and mny:
                all_descriptions.append(desc.replace("\n", " "))
                money.append(mny)
                

with open("expense_classifier_model (1).pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer (1).pkl", "rb") as f:
    cv = pickle.load(f)

results = []
for i, des in enumerate(all_descriptions):
    txt = cv.transform([des])
    pred = model.predict(txt)
    results.append(f"{i} - {des}, {money[i]} --> {pred[0]}")

for result in results:
    print(result)
