from django.shortcuts import render

# Create your views here.
import os
import pickle
import random
import pandas as pd

from django.conf import settings
from django.shortcuts import render


# -------- Load model & data once -------- #

DF_PATH = os.path.join(settings.BASE_DIR, 'mobile_recommender', 'models', 'dataframe.pkl')
SIM_PATH = os.path.join(settings.BASE_DIR, 'mobile_recommender', 'models', 'similarity.pkl')

df = pickle.load(open(DF_PATH, 'rb'))
similarity = pickle.load(open(SIM_PATH, 'rb'))


def fetch_img(index):
    return df['imgURL'].iloc[index]


def recommend_similar(mobile_name):
    idx = df[df['name'] == mobile_name].index[0]
    sims = similarity[idx]

    # top 10 similar (skip itself at [0])
    top10 = sorted(list(enumerate(sims)),
                   key=lambda x: x[1],
                   reverse=True)[1:11]

    data = []
    for i, score in top10:
        data.append({
            'name': df['name'].iloc[i],
            'img': fetch_img(i),
            'rating': df['ratings'].iloc[i],
            'price': df['price'].iloc[i],
        })
    return data


def recommend_different_variety(mobile_name):
    idx = df[df['name'] == mobile_name].index[0]
    sims = similarity[idx]

    sample10 = random.sample(list(enumerate(sims)), k=10)

    data = []
    for i, score in sample10:
        data.append({
            'name': df['name'].iloc[i],
            'img': fetch_img(i),
            'rating': df['ratings'].iloc[i],
            'price': df['price'].iloc[i],
        })
    return data


# -------- Main View -------- #

def home(request):
    mobiles = df['name'].values
    selected_mobile = None
    recommended = []
    other_variety = []

    if request.method == 'POST':
        selected_mobile = request.POST.get('mobile')
        if selected_mobile:
            recommended = recommend_similar(selected_mobile)
            other_variety = recommend_different_variety(selected_mobile)

    context = {
        'mobiles': mobiles,
        'selected_mobile': selected_mobile,
        'recommended': recommended,
        'other_variety': other_variety,
    }
    return render(request, 'index.html', context)
