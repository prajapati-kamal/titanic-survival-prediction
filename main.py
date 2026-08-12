import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300

df = pd.read_csv("C:/Users/DELL/Downloads/train.csv")

print("Shape of training data:", df.shape)
print(df.head())

df["Age"] = df["Age"].fillna(df["Age"].mean())

df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

df["Cabin"] = df["Cabin"].fillna("Unknown")
df["Deck"] = df["Cabin"].str[0]
df = df.drop("Cabin", axis=1)

df.to_csv("C:/Users/DELL/Downloads/train_cleaned.csv", index=False)
print("\nMissing values after cleaning:\n", df.isnull().sum())

def add_features(data):
    data["FamilySize"] = data["SibSp"] + data["Parch"] + 1

    data["IsAlone"] = (data["FamilySize"] == 1).astype(int)

    data["Title"] = data["Name"].str.extract(r",\s*([^.]*)\.")

    data["Title"] = data["Title"].replace(
        ["Lady", "Countess", "Capt", "Col", "Don", "Dr", "Major",
         "Rev", "Sir", "Jonkheer", "Dona"], "Rare"
    )
    data["Title"] = data["Title"].replace(["Mlle", "Ms"], "Miss")
    data["Title"] = data["Title"].replace("Mme", "Mrs")

    return data

df = add_features(df)
print("\nNew features added:", ["FamilySize", "IsAlone", "Title"])
print(df[["FamilySize", "IsAlone", "Title"]].head())

plt.figure(figsize=(7, 5))
sns.barplot(data=df, x='Pclass', y='Survived', hue='Sex')
plt.title('Survival Rate by Passenger Class and Sex')
plt.xlabel('Passenger Class (1 = Highest)')
plt.ylabel('Survival Rate')
plt.tight_layout()
plt.savefig('survival_by_class_sex.png')
plt.show()

plt.figure(figsize=(7, 5))
sns.histplot(data=df, x='Age', hue='Survived', kde=True, alpha=0.6)
plt.title('Age Distribution by Survival')
plt.xlabel('Age')
plt.tight_layout()
plt.savefig('age_distribution.png')
plt.show()

plt.figure(figsize=(8, 6))
numeric_cols = df[['Survived', 'Pclass', 'Age', 'Fare', 'FamilySize']]
sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Feature Correlation Heatmap')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')
plt.show()

features = ["Pclass", "Sex", "Age", "Fare", "Embarked", "Deck",
            "FamilySize", "IsAlone", "Title"]

X = df[features].copy()
y = df["Survived"]

X = pd.get_dummies(X, columns=["Sex", "Embarked", "Deck", "Title"], drop_first=True)

print("\nFinal training columns:", list(X.columns))

X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("\nModel trained successfully!")

val_preds = model.predict(X_val)

print("\nValidation Accuracy:", accuracy_score(y_val, val_preds))
print("\nClassification Report:\n", classification_report(y_val, val_preds))

plt.figure(figsize=(5, 4))
sns.heatmap(confusion_matrix(y_val, val_preds), annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.tight_layout()
plt.savefig('confusion_matrix.png')
plt.show()

importances = pd.Series(model.feature_importances_, index=X_train.columns)
importances = importances.sort_values(ascending=False)

plt.figure(figsize=(8, 6))
sns.barplot(x=importances.values[:10], y=importances.index[:10])
plt.title('Top 10 Most Important Features')
plt.xlabel('Importance')
plt.tight_layout()
plt.savefig('feature_importance.png')
plt.show()

test = pd.read_csv("C:/Users/DELL/Downloads/test.csv")

test["Age"] = test["Age"].fillna(df["Age"].mean())
test["Fare"] = test["Fare"].fillna(df["Fare"].mean())
test["Cabin"] = test["Cabin"].fillna("Unknown")
test["Deck"] = test["Cabin"].str[0]
test["Embarked"] = test["Embarked"].fillna(df["Embarked"].mode()[0])

test = add_features(test)

X_test = test[features].copy()
X_test = pd.get_dummies(X_test, columns=["Sex", "Embarked", "Deck", "Title"], drop_first=True)

X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

test_preds = model.predict(X_test)

submission = pd.DataFrame({
    "PassengerId": test["PassengerId"],
    "Survived": test_preds
})
submission.to_csv("C:/Users/DELL/Downloads/submission.csv", index=False)
print("\nsubmission.csv saved — upload this to the Kaggle competition page")

new_passenger = pd.DataFrame([{
    "Pclass": 3,
    "Sex": "male",
    "Age": 25,
    "SibSp": 0,
    "Parch": 0,
    "Fare": 7.5,
    "Embarked": "S",
    "Cabin": "Unknown",
    "Name": "Mr. Test"
}])

new_passenger["Deck"] = new_passenger["Cabin"].str[0]
new_passenger = add_features(new_passenger)

X_new = new_passenger[features].copy()
X_new = pd.get_dummies(X_new, columns=["Sex", "Embarked", "Deck", "Title"], drop_first=True)
X_new = X_new.reindex(columns=X_train.columns, fill_value=0)

prediction = model.predict(X_new)
probability = model.predict_proba(X_new)

print("\n--- New Passenger Prediction ---")
if prediction[0] == 1:
    print("Prediction: Survived ✅")
else:
    print("Prediction: Did not survive ❌")

print(f"Survival probability: {probability[0][1] * 100:.1f}%")