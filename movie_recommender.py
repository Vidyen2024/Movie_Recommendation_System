import pandas as pd
import numpy as np

# Download the dataset from MovieLens
print("Please download the dataset manually from this link:")
print("https://grouplens.org/datasets/movielens/100k/")

# Load the datasets
# Replace 'path_to_u.data' and 'path_to_u.item' with the dataset file paths after downloading
column_names = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_csv('path_to_u.data', sep='\t', names=column_names, usecols=['user_id', 'movie_id', 'rating'])

movies = pd.read_csv('path_to_u.item', sep='|', header=None, encoding='latin-1', usecols=[0, 1], names=['movie_id', 'title'])

# Merge the datasets
data = pd.merge(ratings, movies, on='movie_id')

# Create a pivot table (rows: movie titles, columns: user IDs, values: ratings)
movie_matrix = data.pivot_table(index='title', columns='user_id', values='rating')

# Function to recommend movies based on user ratings
def recommend_movies(movie_name, num_recommendations=5):
    if movie_name not in movie_matrix.index:
        return "Movie not found in database."

    # Get user ratings for the input movie
    movie_ratings = movie_matrix.loc[movie_name]

    # Compute similarity scores (correlation) with other movies
    similar_movies = movie_matrix.corrwith(movie_ratings)

    # Drop NaN values and sort by similarity
    recommendations = similar_movies.dropna().sort_values(ascending=False).iloc[1:num_recommendations+1]

    return recommendations

# Prompt user for a movie name
print("Enter a movie name (e.g., 'Toy Story (1995)'):")
movie_name = input()
recommendations = recommend_movies(movie_name)

if isinstance(recommendations, str):
    print(recommendations)
else:
    print("Recommended movies:")
    for movie, score in recommendations.items():
        print(f"{movie} (similarity: {score:.2f})")