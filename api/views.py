import asyncio
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from dotenv import load_dotenv
import os
import random
from .utils.scrappers import get_lyrics, clean_text
from .utils.ml import is_phrase_and_song_similar
from .utils.helpers import get_user_playlists, get_user_songs, get_song_suggestions

load_dotenv()

@api_view(['GET'])
def dummy(request):
    return Response(200)


@api_view(['GET'])
def dummy_get(request, num):
    return Response(f"Input: {num}")


@api_view(['POST'])
def dummy_post(request):
    prompt = request.data.get("prompt")
    token = request.data.get("token")
    response = f"you said {prompt} and {token}"
    print(response)
    
    dummy_data = {"songs": [1,2,3,4]}
    
    
    return Response(dummy_data)


@api_view(["GET"])
def login(request):

    params = {
        "response_type": "code",
        "client_id": "dfda70caf6ae465a95ce18a61dc47623",
        "redirect_url": "https://localhost:8000/login",
        "scope": "user-read-private user-read-email",
        "show_dialog": True
    }

    response = requests.get(url="https://accounts.spotify.com/authorize", params=params)


@api_view(["GET"])
def provide_auth_token(request):
    global auth_token
    auth_token = request.GET.get("auth_token")


@api_view(["POST"])
def get_songs(request):
    playlists, status = get_user_playlists(request.data.get('token'))
    
    return Response(data=playlists, status=status)

@api_view(["POST"])
def create_playlist(request):
    token = request.data.get('token')
    phrase = request.data.get('phrase')
    limit = 50

    try:
        limit = int(request.data.get('limit'))
    except:
        None

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    songs = []

    playlists, status = get_user_playlists(token)
    user_tracks, status = get_user_songs(token)

    # print(playlists)
    for playlist in playlists:
        # print(playlist)
        for song in playlist["songs"]:
            songs.append(song)

    for track in user_tracks:
        songs.append(track)

    suggestions, status = get_song_suggestions(token, seed_tracks=[random.choice(songs)["id"] for i in range(3)], seed_artists=[random.choice(songs)["artist_id"] for i in range(2)])

    for track in suggestions:
        songs.append(track)

    matching_songs = []
    count = 0

    for song in songs:
        # through tests threshold of 1 seems good
        lyrics = get_lyrics(song["name"], song["artist_name"])
        print(f"analyzing {song['name']}")
        if is_phrase_and_song_similar(clean_text(phrase), lyrics, 1.0):
            print(f"adding {song['name']}")
            matching_songs.append(song)
            count += 1
        if count >= limit:
            break

    random.shuffle(matching_songs)
    return Response(data=matching_songs, status=200)
