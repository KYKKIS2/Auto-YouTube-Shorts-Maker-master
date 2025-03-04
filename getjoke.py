'''from elevenlabs import generate, play, Voice, VoiceSettings, save

audio = generate(
  text="The Eiffel Tower can be 15 cm taller during the summer. Due to thermal expansion, materials tend to expand when heated.",
  voice=Voice(
        voice_id='pNInz6obpgDQGcFmaJgB',
        settings=VoiceSettings(stability=0.69, similarity_boost=1.0, style=0.0, use_speaker_boost=True)
    ),
  model="eleven_multilingual_v2"
)

play(audio)
save(audio,'test.wav')'''
'''
title = "Testing1"
description = "#funnyvideos #funnyvideosdaily #funnyvideosclips #pubgfunnyvideos #btsfunnyvideos #punjabifunnyvideos #telugufunnyvideos #tiktokfunnyvideos #funnyvideosv #indianfunnyvideos #leagueoflegendsfunnyvideos #funnyvideosclip #kannadafunnyvideos #afghanfunnyvideos #marathifunnyvideos #kevinhartfunnyvideos #dogfunnyvideos #bestfunnyvideos #funnyvideos2018 #funnyvideoshiphop #funnyvideos2019 #hindifunnyvideos #funnyvideosandmemes_ #naijafunnyvideos #funnyvideoslel #tamilfunnyvideos #desifunnyvideos #funnyvideosever #funnyvideostags #pakistanifunnyvideos #funnyvideoswithsuaven2g #blackfunnyvideos #funnyvideosmemes #funnyvideosinhindi #funnyvideoshd #kidsfunnyvideos #funnyvideos2020 #funnyvideosdownload #fortnitefunnyvideos  #funnyvideos2017"

from youtube_upload.client import YoutubeUploader
uploader = YoutubeUploader(secrets_file_path="client_secret.json")

uploader.authenticate()

# Video options
options = {
    "title" : title, # The video title
    "description" : description, # The video description
    "tags" : ["funny jokes","try not to laugh","funny joke story","jokes,joke","jk","laugh","funny videos"],
    "categoryId" : "22",
    "privacyStatus" : "private", # Video privacy. Can either be "public", "private", or "unlisted"
    "kids" : False, # Specifies if the Video if for kids or not. Defaults to False.
}

file_path = "test_videos/" + title + ".mp4"

# upload video
uploader.upload(file_path, options) '''
import os,re,string,json

def clean_joke(title, selftext):
    # Remove content after "Edit:" or "EDIT:" (case insensitive)
    edit_pattern = re.compile(r'\bEDIT\b:', re.IGNORECASE)
    selftext = re.split(edit_pattern, selftext)[0].strip()

    # Check if the title ends with a period, if not, add one
    if not title.endswith('.'):
        title += '.'

    # Check if the title is repeated in the beginning of the selftext
    # We use 're.escape' to handle any special characters in the title
    if selftext.lower().startswith(re.escape(title.lower())):
        selftext = selftext[len(title):].strip()

    # Combine and return the cleaned title and selftext
    final_text = f"{title} {selftext}".strip()
    return final_text, title, selftext

def sanitize_filename(filename):
    # Define the characters to whitelist
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    # Replace any invalid character with an underscore
    cleaned_filename = re.sub(f'[^{re.escape(valid_chars)}]', '_', filename)
    return cleaned_filename

def title_exists(title, directory):
    max_length = 100
    if len(title) > max_length:
        title = title[:max_length]
        title = sanitize_filename(title)
        print(title)
    # Sanitize the title to remove any characters that are invalid in file names
    sanitized_title = sanitize_filename(title)
    #print(sanitized_title)
    # Check if file exists
    file_path = os.path.join(directory, sanitized_title + ".mp4")
    #print(file_path)
    return os.path.isfile(file_path)

import requests,json,random

def authenticate(client_id, secret, appname, username, password):
    # This function handles the authentication and returns the header required to make requests
    auth = requests.auth.HTTPBasicAuth(client_id, secret)
    creds = {
        'grant_type':'password',
        'username': username,
        'password': password,
    }
    headers = {'User-Agent': appname}
    req = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=creds, headers=headers)
    TOKEN = req.json()['access_token']
    headers['Authorization'] = f"bearer {TOKEN}"
    return headers

import requests
import json
import random,html

# Rest of your code...

def save_jokes(jokes_list, filepath="saved_jokes.json"):
    with open(filepath, 'w') as file:
        json.dump(jokes_list, file)

def load_saved_jokes(filepath="saved_jokes.json"):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as file:
        return json.load(file)

def get_random_joke(client_id, secret, appname, username, password, upvote_threshold=50):
    headers = authenticate(client_id, secret, appname, username, password)
    final_suitable_jokes = []
    saved_jokes = load_saved_jokes("saved_jokes.json")
    # Fetch top posts of the week from r/jokes
    after = None  # Initialize 'after' to None

    for i in range(30):
        if i == 0:
            response = requests.get('https://oauth.reddit.com/r/Jokes/top?t=all&limit=100', headers=headers)
        # Subsequent requests use the 'after' parameter
        else:
            # Include the value of `after` in the URL
            response = requests.get(f'https://oauth.reddit.com/r/Jokes/top?t=all&limit=100&after={after}', headers=headers)
        
        data = response.json()['data']
        jokes = data['children']
        after = data.get('after')  # Use .get() to avoid KeyError if 'after' is missing
    
        
        print(f"Iteration {i}, using after: {after}")
        print(f"Found {len(jokes)} jokes.")
        print(f"New after for next iteration: {data['after']}")
        # Filter jokes within the character length limit and by upvotes
        suitable_jokes = [
            joke for joke in jokes
            if 200 <= len(joke['data']['title']) + len(joke['data']['selftext']) <= 500
            and joke['data']['ups'] >= upvote_threshold
        ]
        if after is None:
            print(f"No more posts to fetch after iteration {i}.")
            break
        final_suitable_jokes += suitable_jokes
        
        

    if not final_suitable_jokes:
        #print("No suitable jokes found.")
        return

    print(f"Found {len(final_suitable_jokes)} suitable jokes after filtering by character length and upvotes.")
    
    for joke in final_suitable_jokes:
        suitable_joke = joke['data'] 
        title = suitable_joke['title']
        print("Suit Jokes:",title)
        selftext = suitable_joke['selftext'].replace('\n', ' ').replace('\r', ' ')
        final_text = title+"."+selftext
        if title_exists(title, "Tobeuploaded/"):
            print("Title exists!1")
            continue
        else:
            # Save the new joke
            save_jokes(saved_jokes, "saved_jokes.json")
            final_text,title,selftext = clean_joke(title, selftext)
            print("Finaltext: ",final_text)
            print("Title: ",title)
            print("Selftext: ",selftext)
            return final_text, title, selftext

    #for jokes in final_suitable_jokes:
        #print(jokes)
   
    '''    # Randomly select one of the suitable jokes
    final_suitable_jokes = random.choice(final_suitable_jokes)['data']
    title = final_suitable_jokes['title']
    selftext = final_suitable_jokes['selftext'].replace('\n', ' ').replace('\r', ' ')
    final_text = title+"."+selftext

    if( title_exists(title, "Tobeuploaded/")):
      print("Title exists!1")
      return None
    else:
      return final_text,title,selftext
    '''


if __name__ == "__main__":
    # Code you want to run only when executing test.py directly
    # For example, calling get_random_joke and printing the result

    # Replace the following variables with your Reddit app details and user credentials
    with open(r'C:\Users\kykki\Documents\OneDrive\Documents\Youtube\Auto-YouTube-Shorts-Maker-master\reddit-downloader-main\config.json', 'r') as f:
            CONFIG = json.load(f)

    CLIENT_ID = CONFIG['client_id']
    SECRET = CONFIG['secret']
    APPNAME = CONFIG['appname']
    USERNAME = CONFIG['username']
    PASSWORD = CONFIG['password']
    result = get_random_joke(CLIENT_ID, SECRET, APPNAME, USERNAME, PASSWORD)
    if result is None:
        # Handle the case where no joke was found
        print("No joke found, exiting or trying again.")
        while result is None:
            result = get_random_joke(CLIENT_ID, SECRET, APPNAME, USERNAME, PASSWORD)
        print(result)
    else:
        final_text, title1, content = result
        print(title1)