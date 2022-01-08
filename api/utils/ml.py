from math import sqrt
import requests
import string
import os

def get_vector_distance(v1, v2) -> float:
    distance1squared = sum(x**2 for x in v1)
    distance2squared = sum(x**2 for x in v2)

    return sqrt(distance1squared - distance2squared)

def convert_text_to_vector(text: str):
    data = {"text": text}

    r = requests.get(os.environ.get("COLAB_SERVER_URL") + "/vector", json=data)

    r = r.json()

    print(r)

    return r["vector"]

def get_phrase_and_song_similarity(phrase: str, song_id: str) -> float:
    # get song lyrics from scraping
    song_lyrics = """
    Is this the real life?
Is this just fantasy?
Caught in a landside,
No escape from reality
Open your eyes,
Look up to the skies and see,
I'm just a poor boy, I need no sympathy,
Because I'm easy come, easy go,
Little high, little low,
Any way the wind blows doesn't really matter to
Me, to me
Mamaaa,
Just killed a man,
Put a gun against his head, pulled my trigger,
Now he's dead
Mamaaa, life had just begun,
But now I've gone and thrown it all away
Mama, oooh,
Didn't mean to make you cry,
If I'm not back again this time tomorrow,
Carry on, carry on as if nothing really matters
Too late, my time has come,
Sends shivers down my spine, body's aching all
The time
Goodbye, everybody, I've got to go,
Gotta leave you all behind and face the truth
Mama, oooh
I don't want to die,
I sometimes wish I'd never been born at all.
I see a little silhouetto of a man,
Scaramouch, Scaramouch, will you do the Fandango!
Thunderbolts and lightning, very, very frightening me
Galileo, Galileo
Galileo, Galileo
Galileo, Figaro - magnificoo
I'm just a poor boy nobody loves me
He's just a poor boy from a poor family,
Spare him his life from this monstrosity
Easy come, easy go, will you let me go
Bismillah! No, we will not let you go
(Let him go!) Bismillah! We will not let you go
(Let him go!) Bismillah! We will not let you go
(Let me go) Will not let you go
(Let me go)(Never) Never let you go
(Let me go) (Never) let you go (Let me go) Ah
No, no, no, no, no, no, no
Oh mama mia, mama mia, mama mia, let me go
Beelzebub has a devil put aside for me, for me,
For meee
So you think you can stop me and spit in my eye
So you think you can love me and leave me to die
Oh, baby, can't do this to me, baby,
Just gotta get out, just gotta get right outta here
Nothing really matters, Anyone can see,
Nothing really matters,
Nothing really matters to me
Any way the wind blows...
    """
    

    # convert to vectors
    phrase_vector = convert_text_to_vector(phrase)
    lyrics_vector = convert_text_to_vector(song_lyrics)

    return abs(get_vector_distance(phrase_vector, lyrics_vector))

def is_phrase_and_song_similar(phrase: str, song_id: str, threshold: float) -> bool:
    if (get_phrase_and_song_similarity(phrase, song_id) <= threshold):
        return True

    return False
