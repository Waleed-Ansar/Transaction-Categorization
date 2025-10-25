import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


df = pd.read_csv("/content/transaction_training_data.csv")
df = df.fillna('Uncategorized')

X_train, X_test, y_train, y_test = train_test_split(df.Description, df.Category, test_size=0.2)

cv = CountVectorizer()

X_train_cv = cv.fit_transform(X_train.values)
X_test_cv = cv.transform(X_test.values)


model = MultinomialNB()

model.fit(X_train_cv, y_train)

txt = cv.transform(["POS Debit- Business Debit Card 1969 09-13-23 Amzn Mktp Us*tr1Dx Amzn.Com/Bill WA"])

y_pred = model.predict(txt)


with open("expense_classifier_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(cv, f)
y_pred
