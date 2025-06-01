#Importing libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


#out directory (project folder)
os.makedirs('output_images', exist_ok=True)

#Loading the data
df = pd.read_csv('netflix_titles.csv')


#Cleaning - preview and check missing values
print("First 5 rows:\n", df.head())
print("\nMissing values:\n", df.isnull().sum())

#replace missing values
for column in ['country', 'rating', 'cast', 'director']:
    df[column].fillna('Unknown', inplace=True)

#Drop rows where 'date_added' is missing for time analysis
df = df.dropna(subset=['date_added'])

#Convert date to datetime
df['date_added'] = pd.to_datetime(df['date_added'], errors = 'coerce')
df['year_added'] = df['date_added'].dt.year

#check again for missing value
print("\nMIssing values after cleaning:\n", df.isnull().sum())


#Plot: Relationship between TV Shows and Movies
plt.figure(figsize=(6, 4))
sns.countplot(x='type', data=df)
plt.title('TV Shows vs Movies on Netflix')
plt.savefig('output_images/type_distribution.png')
plt.close()

#Top 10 Content-Producing Countries
top_countries = df['country'].value_counts().head(10)
top_countries.plot(kind='barh', color='orange')
plt.title('Top 10 Content Producing Countries')
plt.xlabel('Number of Titles')
plt.tight_layout()
plt.savefig('output_images/top_countries.png')
plt.close()

#Content Added Over Time
yearly =df['year_added'].value_counts().sort_index()
yearly.plot(marker = 'o', linewidth=2)
plt.title('Netflix Content Added Over Time')
plt.xlabel('Year')
plt.ylabel('Number Of Titles')
plt.grid(True)
plt.savefig('output_images/content_over_time.png')
plt.close()

#Top 10 Content Ratings
plt.figure(figsize=(8, 4))
sns.countplot(y='rating', data=df, order=df['rating'].value_counts().index[:10])
plt.title('Top 10 Content Ratings')
plt.savefig('output_images/top_ratings.png')
plt.close()

#Top Genres
genre_series = df['listed_in'].dropna().str.split(', ')
all_genres =genre_series.explode()
top_genres = all_genres.value_counts().head(10)

plt.figure(figsize=(8, 4))
sns.barplot(x=top_genres.values, y=top_genres.index, palette="coolwarm")
plt.title('Top 10 Most Common Genres on Netflix')
plt.xlabel('Number of Titles')
plt.ylabel('Genre')
plt.tight_layout()
plt.savefig('output_images/top_genres.png')
plt.close()

print("✅ Analysis complete. Charts saved in 'output_images/' folder.")