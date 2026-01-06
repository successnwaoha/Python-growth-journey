import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report

# 1. Load Data
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# 2. Select Features (The data we use to predict)
# Target (y) is 'Survived', Features (X) are the rest
features = ['Pclass', 'Sex', 'Age', 'Fare', 'SibSp', 'Parch']
X = df[features]
y = df['Survived']

# 3. Preprocessing (The Cleaning Factory)
# For numbers: fill missing with average, then scale
numeric_transformer = Pipeline(steps=[
    ('importer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# For categories: fill missing, then turn into 1s and 0s
categorical_transformer = Pipeline(steps=[
    ('importer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, ['Age', 'Fare', 'SibSp', 'Pclass', 'Parch']),
    ('cat', categorical_transformer, ['Sex'])
])

# 4. The Full Pipeline (Preprocess + Model)
clf = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100))
])

# 5. Split and Train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf.fit(X_train, y_train)

# 6. Evaluate
y_pred = clf.predict(X_test)
print("--- Confusion Matrix ---")
print(confusion_matrix(y_test, y_pred))
print("\n--- Report ---")
print(classification_report(y_test, y_pred))

# 7. Save the Model
joblib.dump(clf, 'titanic_model.pkl')
print("\nModel saved as titanic_model.pkl")