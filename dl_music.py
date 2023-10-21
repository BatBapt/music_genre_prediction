import requests
import re
import unidecode
import os, sys


def get_cover_from_url(url, filename):
    """
    Get the album cover from the url and filename.

    :args: url: str -> url of the album
    :args: filename: str -> filename to write
    """
    response = requests.get(url)

    if response.status_code == 200:
        image_content = response.content

        with open(filename, "wb") as f:
            f.write(image_content)
    else:
        print("Something went wrong when trying to download the cover: {}".format(url))
        sys.exit()


def get_preview_from_url(url, filename):
    """
    Get the preview of the music (30sec) from the url and filename.

    :args: url: str -> url of the sound
    :args: filename: str -> filename to write
    """
    response = requests.get(url)
    
    if response.status_code == 200:
        audio_content = response.content

        with open(filename, "wb") as f:
            f.write(audio_content)
    else:
        print("Something went wrong when trying to download audio preview: {}".format(url))
        sys.exit()
    

def get_data_from_type(url_playlist, genre="rock"):
    """
    Main function.

    Given an url playlist and the music genre, download the cover of every album in it + 30sec of music.

    :args: url_playlist: str -> url to the Deezer playlist using their API
    :args: genre: str -> genre of the music (used to sort data)
    """
    if not os.path.exists("images/{}".format(genre)):
        os.mkdir("images/{}".format(genre))
    if not os.path.exists("audio/{}".format(genre)):
        os.mkdir("audio/{}".format(genre))

    response = requests.get(url_playlist)

    data = response.json()

    tracks = data["tracks"]["data"]
    n = len(tracks)
    for index, track in enumerate(tracks):
        preview_url = track["preview"]
        url_img = track["album"]["cover_medium"] 

        if len(preview_url) != 0 and len(url_img) != 0:
            # Text transformation 
            title = track["album"]["title"].lower()
            title = re.sub(r'[!.,;:?()&*/_><"]', '', title)
            title = unidecode.unidecode(title)
            splited = title.split()

            path_img = "images/{}/{}.png".format(genre, "_".join(splited))
            get_cover_from_url(url_img, path_img)

            path_audio = "audio/{}/{}.mp3".format(genre, "_".join(splited))
            get_preview_from_url(preview_url, path_audio)
        
        if index%20 == 0:
            print("Music {}: {}/{}".format(genre, index, n))


def get_album(url_album):
    """
    Function used to download 1 album (cover + audio preview) to test the model.
    Store them in the 'test' directory 

    :args: url_album: str -> url to the Deezer album using their API

    """
    response = requests.get(url_album)
    
    if response.status_code == 200:
        data = response.json()
        img_url = data["cover_medium"]
        get_cover_from_url(img_url, "test/test.png")
        tracks = data["tracks"]["data"][0]
        get_preview_from_url(tracks["preview"], "test/test.mp3")
    else:
        print("Something went wrong when trying to download data")
        sys.exit()

def get_info():
    """
    Get informations on the music downloaded in the directory 'images' and 'audio'
    """
    s = 0
    print("Images")
    for dir in os.listdir("images"):
        nb = len(os.listdir("images/{}".format(dir)))
        print("\tNombre de fichier dans {}: {}".format(dir, nb))
        s += nb

    print("Nombre total de fichier: {}".format(s))
    
    print("Audio")
    for dir in os.listdir("Audio"):
        nb = len(os.listdir("audio/{}".format(dir)))
        print("\tNombre de fichier dans {}: {}".format(dir, nb))


def dl_all():
    """
    Downloads every playlist from the dictionary under using Deezer API
    """
    dico_music = {
        #"rap": ['6791265584', '3272614282', '6156189524'],
        #"rock": ["1306931615", "8882778922", "606864095", "7752679842"],
        #"jazz": ['1615514485', '8055116382', '7420751724', '7867312122', '1450192665', '591596525', "10371376882"],
        #"rnb": ["10023969882", "6754766424"],
        "dubstep": ["1979182002", "58244468"],
    }
    for genre, value in dico_music.items():
        for playlist_id in value:
            url_playlist = "https://api.deezer.com/playlist/{}".format(playlist_id)
            get_data_from_type(url_playlist, genre)
            print("\tFin playlist {}".format(playlist_id))
        print("Fin {}".format(genre))