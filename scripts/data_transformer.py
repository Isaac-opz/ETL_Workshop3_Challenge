import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

df_2015 = pd.read_csv('data/2015.csv')
df_2016 = pd.read_csv('data/2016.csv')
df_2017 = pd.read_csv('data/2017.csv')
df_2018 = pd.read_csv('data/2018.csv')
df_2019 = pd.read_csv('data/2019.csv')

def standardize_columns(df, year):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace(r'\W', '')
    if year in [2015, 2016]:
        df.rename(columns={
            'economy_(gdp_per_capita)': 'gdp_per_capita',
            'health_(life_expectancy)': 'healthy_life_expectancy',
            'trust_(government_corruption)': 'perceptions_of_corruption'
        }, inplace=True)
    if year == 2017:
        df.rename(columns={
            'happiness.rank': 'happiness_rank',
            'happiness.score': 'happiness_score',
            'economy..gdp.per.capita.': 'gdp_per_capita',
            'health..life.expectancy.': 'healthy_life_expectancy',
            'trust..government.corruption.': 'perceptions_of_corruption'
        }, inplace=True)
    if year in [2018, 2019]:
        df.rename(columns={
            'country_or_region': 'country',
            'score': 'happiness_score',
            'overall_rank': 'happiness_rank'
        }, inplace=True)
    return df

dfs = [df_2015, df_2016, df_2017, df_2018, df_2019]
years = [2015, 2016, 2017, 2018, 2019]
dfs = [standardize_columns(df, year) for df, year in zip(dfs, years)]

all_data = pd.concat(dfs, keys=years, names=['year'])
all_data.reset_index(level=1, drop=True, inplace=True)
all_data.reset_index(inplace=True)


numeric_cols = all_data.select_dtypes(include=[np.number]).columns
non_numeric_cols = all_data.select_dtypes(exclude=[np.number]).columns

all_data[numeric_cols] = all_data[numeric_cols].fillna(all_data[numeric_cols].mean())
all_data[non_numeric_cols] = all_data[non_numeric_cols].fillna(all_data[non_numeric_cols].mode().iloc[0])

all_data.dropna(inplace=True)

all_data['gdp_health_interaction'] = all_data['gdp_per_capita'] * all_data['healthy_life_expectancy']

all_data['log_gdp_per_capita'] = np.log1p(all_data['gdp_per_capita'])
all_data['log_social_support'] = np.log1p(all_data['social_support'])

features = ['log_gdp_per_capita', 'log_social_support', 'healthy_life_expectancy', 
            'freedom_to_make_life_choices', 'generosity', 'perceptions_of_corruption', 'gdp_health_interaction']
target = 'happiness_score'

X = all_data[features]
y = all_data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

test_data = all_data.loc[X_test.index]
test_data.to_csv('data/transformed_test_data.csv', index=False)
