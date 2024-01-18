import os
from django import forms
from django.shortcuts import render
from .forms import UserInputForm
import surprise
from surprise import Reader, Dataset, SVD, dump
from surprise.model_selection import train_test_split
import pandas as pd

def get_recommendations_for_user(user_id):
    reader = Reader(rating_scale=(1, 5))
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    movies = pd.read_csv(os.path.join(data_path, 'movies.csv'))
    merged_data_sorted = pd.read_parquet(os.path.join(data_path, 'smalldata.parquet'))
    data = Dataset.load_from_df(merged_data_sorted[['userId', 'movieId', 'rating']], reader)
    algo, trainset = dump.load(os.path.join(data_path, 'algorithm.pkl'))
    recommendations = []

    user_ratings = merged_data_sorted[merged_data_sorted['userId'] == int(user_id)][['movieId', 'rating']]
    movies_rated_by_user = user_ratings['movieId'].tolist()
    all_movie_ids = data.build_full_trainset().all_items()
    movies_to_predict = list(set(all_movie_ids) - set(movies_rated_by_user))

    user_predictions = [algo.predict(int(user_id), movie_id) for movie_id in movies_to_predict]
    user_predictions_sorted = sorted(user_predictions, key=lambda x: x.est, reverse=True)
    
    top_n = 5
    for i in range(min(top_n, len(user_predictions_sorted))):
        movie = user_predictions_sorted[i]
        movie_name = movies[movies['movieId'] == movie.iid]['title'].values[0]
        recommendations.append(f"Movie Name: {movie_name}, Estimated Rating: {movie.est}")

    return recommendations

class UserInputForm(forms.Form):
    user_id = forms.IntegerField()

def get_movie_recommendations(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            recommendations = get_recommendations_for_user(user_id)
            return render(request, 'recommendations.html', {'user_id': user_id, 'recommendations': recommendations})
    else:
        form = UserInputForm()

    return render(request, 'input_form.html', {'form': form})
