# Import everything
from youtube_upload.client import YoutubeUploader
from dotenv import load_dotenv
import random
import os
import openai
from gtts import gTTS
from moviepy.editor import *
import moviepy.video.fx.crop as crop_vid
from elevenlabs import generate, play, Voice, VoiceSettings, save, set_api_key,get_api_key
from main import *
import shutil
from getjoke import get_random_joke
import json,string,re,time

#You can also add as many API keys as you want from ElevenLabs and when one is out of characters because of API limits,
#it can iterate to the next API key. 
#Example of .env file:
#ELEVEN_API_KEY_1="" #user@g.
#ELEVEN_API_KEY_2="" #user@g.
#ELEVEN_API_KEY_3="" #user@g.
#ELEVEN_API_KEY_4="" #user@

load_dotenv()
api_keys = [os.getenv(f'ELEVEN_API_KEY_{i}') for i in range(1, 6)]  # Adjust the range as needed for your keys
current_key_index = 0

for i in range(100):
    

    def sanitize_filename(filename):
        # Define the characters to whitelist
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        # Replace any invalid character with an underscore
        cleaned_filename = re.sub(f'[^{re.escape(valid_chars)}]', '_', filename)
        return cleaned_filename

    with open(r'C:\Users\kykki\Documents\OneDrive\Documents\Youtube\Auto-YouTube-Shorts-Maker-master\reddit-downloader-main\config.json', 'r') as f:
            CONFIG = json.load(f)

    CLIENT_ID = CONFIG['client_id']
    SECRET = CONFIG['secret']
    APPNAME = CONFIG['appname']
    USERNAME = CONFIG['username']
    PASSWORD = CONFIG['password']



    # Ask for video info
    #title = input("\nEnter the name of the video >  ")
    #option = input('Do you want AI to generate content? (yes/no) >  ')
    description = "#funnyvideos #funnyvideosdaily #funnyvideosclips #pubgfunnyvideos #btsfunnyvideos #punjabifunnyvideos #telugufunnyvideos #tiktokfunnyvideos #funnyvideosv #indianfunnyvideos #leagueoflegendsfunnyvideos #funnyvideosclip #kannadafunnyvideos #afghanfunnyvideos #marathifunnyvideos #kevinhartfunnyvideos #dogfunnyvideos #bestfunnyvideos #funnyvideos2018 #funnyvideoshiphop #funnyvideos2019 #hindifunnyvideos #funnyvideosandmemes_ #naijafunnyvideos #funnyvideoslel #tamilfunnyvideos #desifunnyvideos #funnyvideosever #funnyvideostags #pakistanifunnyvideos #funnyvideoswithsuaven2g #blackfunnyvideos #funnyvideosmemes #funnyvideosinhindi #funnyvideoshd #kidsfunnyvideos #funnyvideos2020 #funnyvideosdownload #fortnitefunnyvideos  #funnyvideos2017"
    option = 'no'

    if option == 'yes':
        # Generate content using OpenAI API
        theme = input("\nEnter the theme of the video >  ")

        ### MAKE .env FILE AND SAVE YOUR API KEY ###
        openai.api_key = os.environ["OPENAI_API"]
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Generate content on - \"{theme}\"",
            temperature=0.7,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        print(response.choices[0].text)

        yes_no = input('\nIs this fine? (yes/no) >  ')
        if yes_no == 'yes':
            content = response.choices[0].text
        else:
            content = input('\nEnter >  ')
    else:
        #content = input('\nEnter the content of the video >  ')
        result = None
        while result is None:
            try:
                result = get_random_joke(CLIENT_ID, SECRET, APPNAME, USERNAME, PASSWORD)
                if result is None:
                    print("No joke found or title exists, retrying...")
                    # Optionally, add a sleep here to avoid hitting the rate limit
                    time.sleep(1)
            except KeyError as e:
                print(f"An error occurred: {e}. Retrying...")
                # Optionally, add a sleep here to avoid hitting the rate limit
                time.sleep(1)

            
        
        final_text, title1, content = result
        max_length = 100

        # Cut the title to the max_length if necessary
        if len(title1) > max_length:
            title = title1[:max_length]
            title = sanitize_filename(title)
            content = final_text
            print(title)
        else:
            title = sanitize_filename(title1)
            content = final_text
            print(title)

    # Create the directory
    if os.path.exists('test_videos') == False:
        os.mkdir('test_videos')

    flag = True
    attempted_api_keys = 0
    while (flag == True) and attempted_api_keys < len(api_keys):
        try:
            print(f"Attempting with API key index: {current_key_index}, Attempt number: {attempted_api_keys}")
            #Generate voice for Adam
            audio = generate(
            text=content,api_key=api_keys[current_key_index],
            voice=Voice(
                    voice_id='pNInz6obpgDQGcFmaJgB',
                    settings=VoiceSettings(stability=0.69, similarity_boost=1.0, style=0.0, use_speaker_boost=True)
                ),
            model="eleven_multilingual_v2"
            )
            save(audio,'test_videos/adam.wav')

            # Generate speech for the video
            speech = gTTS(text=content, lang='en', tld='ca', slow=False)
            gp = random.choice(["1", "2"])
            audio_clip = AudioFileClip("test_videos/adam.wav")
            video_length = 4800
            max_start = max(1, video_length - int(audio_clip.duration) - 1)
            start_point = random.randint(1, max_start)
            

            if (audio_clip.duration + 1.3 > 58):
                print('\nSpeech too long!\n' + str(audio_clip.duration) + ' seconds\n' + str(audio_clip.duration + 1.3) + ' total')
                exit()

            print('\n')

            ### VIDEO EDITING ###

            # Trim a random part of minecraft gameplay and slap audio on it
            video_clip = VideoFileClip("gameplay/gameplay_1" + ".mp4").subclip(start_point, start_point + audio_clip.duration + 1.3)
            final_clip = video_clip.set_audio(audio_clip)

            # Resize the video to 9:16 ratio
            w, h = final_clip.size
            target_ratio = 1080 / 1920
            current_ratio = w / h

            if current_ratio > target_ratio:
                # The video is wider than the desired aspect ratio, crop the width
                new_width = int(h * target_ratio)
                x_center = w / 2
                y_center = h / 2
                final_clip = crop_vid.crop(final_clip, width=new_width, height=h, x_center=x_center, y_center=y_center)
            else:
                # The video is taller than the desired aspect ratio, crop the height
                new_height = int(w / target_ratio)
                x_center = w / 2
                y_center = h / 2
                final_clip = crop_vid.crop(final_clip, width=w, height=new_height, x_center=x_center, y_center=y_center)

            # Write the final video
            final_clip.write_videofile("test_videos/" + title + ".mp4", codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
            flag = False
        except Exception as e:
            error_message = str(e)
            print(f"An error occurred: {error_message}")

            if "This request exceeds your quota" in error_message:
                print("Character limit reached, switching to next API key...")
                current_key_index = (current_key_index + 1) % len(api_keys)
                attempted_api_keys += 1
                print(f"Switched to API key index: {current_key_index}, Attempt number: {attempted_api_keys}")
            else:
                # If the exception is not related to the quota, exit the loop
                flag = False
        if attempted_api_keys >= len(api_keys):
            print("All API keys have been attempted and have exceeded their quota.")

    # Example usage
    model_path = "base"
    video_path = "test_videos/"+title+".mp4"
    output_video_path = "test_videos/"+title+".mp4"
    output_audio_path = "test_videos/adam.wav"
        
    transcriber = VideoTranscriber(model_path, video_path)
    transcriber.extract_audio()
    transcriber.transcribe_video()
    transcriber.create_video(output_video_path,audio_clip.duration,background_music_path="test_videos\WiiMusic.mp3")

    src =  "test_videos/"+title+".mp4"
    shutil.copy(src,"Tobeuploaded")

    file_path = "Tobeuploaded/" + title + ".mp4"

    #Transfer file to Ubuntu Linux Server YTuploader
    import paramiko

    file_path = "Tobeuploaded/" + title + ".mp4"
    # Set up the connection parameters
    hostname = 'ec2-13-50-17-236.eu-north-1.compute.amazonaws.com'
    port = 22
    username = 'ubuntu'
    local_file = file_path
    remote_path = '/home/ubuntu/YTuploader/Tobeuploaded/' + title + ".mp4"
    key_file_path = 'Testi1.pem'

    # Initialize the SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the server
    try:
        client.connect(hostname, port=port, username=username, key_filename=key_file_path)

        # Use SFTP to transfer the file
        sftp = client.open_sftp()
        sftp.put(local_file, remote_path)
        sftp.close()

        print("File transferred successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

'''
uploader = YoutubeUploader(secrets_file_path="client_secret.json")

#uploader.authenticate()

# Video options
options = {
    "title" : title, # The video title
    "description" : description, # The video description
    "tags" : ["funny jokes","try not to laugh","funny joke story","jokes,joke","jk","laugh","funny videos"],
    "categoryId" : "23",
    "privacyStatus" : "private", # Video privacy. Can either be "public", "private", or "unlisted"
    "kids" : False, # Specifies if the Video if for kids or not. Defaults to False.
}

file_path = "Tobeuploaded/" + title + ".mp4"

# upload video
uploader.upload(file_path, options) 
'''
