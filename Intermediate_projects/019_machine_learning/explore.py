import pandas as pd

# Load a sample dataset (Titanic is the classic starter)
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

print(df.head())     # See first 5 rows
print(df.info())     # See which columns have missing data
print(df.describe()) # See averages, min, max