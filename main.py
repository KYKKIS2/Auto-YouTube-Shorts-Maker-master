import whisper
import os
import shutil
import cv2
from moviepy.editor import ImageSequenceClip, AudioFileClip, VideoFileClip
from tqdm import tqdm
from moviepy.editor import CompositeAudioClip

FONT = cv2.FONT_HERSHEY_DUPLEX
FONT_SCALE = 2.2
FONT_THICKNESS = 3

class VideoTranscriber:
    def __init__(self, model_path, video_path):
        self.model = whisper.load_model(model_path)
        self.video_path = video_path
        self.audio_path = ''
        self.text_array = []
        self.fps = 0
        self.char_width = 0

    def transcribe_video(self):
        print('Transcribing video')
        result = self.model.transcribe(self.audio_path)
        text = result["segments"][0]["text"]
        textsize = cv2.getTextSize(text, FONT, FONT_SCALE, FONT_THICKNESS)[0]
        cap = cv2.VideoCapture(self.video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        asp = 16/9
        ret, frame = cap.read()
        width = frame[:, int(int(width - 1 / asp * height) / 2):width - int((width - 1 / asp * height) / 2)].shape[1]
        width = width - (width * 0.1)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.char_width = int(textsize[0] / len(text))
        #print("out")
        for j in tqdm(result["segments"]):
            #print("in")
            lines = []
            text = j["text"]
            end = j["end"]
            start = j["start"]
            total_frames = int((end - start) * self.fps)
            start = start * self.fps
            total_chars = len(text)
            words = text.split(" ")
            i = 0
            
            while i < len(words):
                #print("i =", i)
                words[i] = words[i].strip()
                if words[i] == "":
                    i += 1
                    continue

                # Initialize remaining_pixels for a new line
                remaining_pixels = width  # Assume 'width' is the max line width in pixels

                line = words[i]  # Start a new line with the first word
                length_in_pixels = (len(words[i]) + 1) * self.char_width
                remaining_pixels -= length_in_pixels  # Update remaining pixels after adding the first word

                i += 1  # Increment i to move to the next word after adding the first word to the line

                while remaining_pixels > 0 and i < len(words):
                    length_in_pixels = (len(words[i]) + 1) * self.char_width
                    if remaining_pixels >= length_in_pixels:
                        line += " " + words[i]  # Add the word to the line
                        remaining_pixels -= length_in_pixels  # Update remaining pixels
                    else:
                        # If the word would overflow the line, stop adding words and prepare to create a new line
                        break

                    i += 1  # Increment i to move to the next word for the current line or the next line

                
                line_array = [line, int(start) + 15, int(len(line) / total_chars * total_frames) + int(start) + 15]
                start = int(len(line) / total_chars * total_frames) + int(start)
                lines.append(line_array)
                self.text_array.append(line_array)
        
        cap.release()
        print('Transcription complete')
    
    def extract_audio(self):
        print('Extracting audio')
        audio_path = "adam.wav"
        video = VideoFileClip(self.video_path)
        audio = video.audio 
        audio.write_audiofile(audio_path)
        self.audio_path = audio_path
        print('Audio extracted')
    
    def extract_frames(self, output_folder):
        print('Extracting frames')
        cap = cv2.VideoCapture(self.video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        asp = width / height
        N_frames = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = frame[:, int(int(width - 1 / asp * height) / 2):width - int((width - 1 / asp * height) / 2)]

            for i in self.text_array:
                if N_frames >= i[1] and N_frames <= i[2]:
                    text = i[0].upper()
                    # Use the initialized font scale and thickness
                    text_size, _ = cv2.getTextSize(text, FONT, FONT_SCALE, FONT_THICKNESS)
                    text_x = int((frame.shape[1] - text_size[0]) / 2)
                    text_y = int((height / 2) + (text_size[1] / 2))  # Make sure this is an int

                    # Draw the outline
                    cv2.putText(frame, text, (text_x, text_y), FONT, FONT_SCALE, (0, 0, 0), FONT_THICKNESS+23, lineType=cv2.LINE_AA)

                    # Draw the main text
                    cv2.putText(frame, text, (text_x, text_y), FONT, FONT_SCALE, (255, 255, 255), FONT_THICKNESS, lineType=cv2.LINE_AA)
                    break

            cv2.imwrite(os.path.join(output_folder, str(N_frames) + ".jpg"), frame)
            N_frames += 1

        cap.release()
        print('Frames extracted')


    def create_video(self, output_video_path, audio_duration, background_music_path):
        print('Creating video')
        image_folder = os.path.join(os.path.dirname(self.video_path), "frames")
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        
        self.extract_frames(image_folder)
        
        images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
        images.sort(key=lambda x: int(x.split(".")[0]))
        
        # Load images as a sequence
        clip = ImageSequenceClip([os.path.join(image_folder, image) for image in images], fps=self.fps)
        
        # Load the audio
        audio = AudioFileClip(self.audio_path)
        
        # Make sure the video clip does not exceed the audio duration
        if clip.duration > audio_duration:
            clip = clip.subclip(0, audio_duration)
        
        # Load the main audio
        main_audio = AudioFileClip(self.audio_path).set_duration(audio_duration)
        
        # Load the background music
        background_music = AudioFileClip(background_music_path).volumex(0.4)  # Reduce the volume
        # Ensure the background music matches the main audio duration
        background_music = background_music.set_duration(audio_duration)
        
        # Combine the main audio and the background music
        final_audio = CompositeAudioClip([main_audio, background_music])

        # Set the audio to the video clip
        final_clip = clip.set_audio(final_audio.set_duration(audio_duration))

        # Write the final video file with the adjusted duration
        final_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac', remove_temp=True)
        
        shutil.rmtree(image_folder)
        #os.remove(os.path.join(os.path.dirname(self.video_path), "adam.wav"))

'''
# Example usage
model_path = "base"
video_path = "test_videos/CAN THE ADMINS OF THIS GROUP DO A BETTER JOB OF MONITORING WHO IS ALLOWED IN HERE PLEASE__.mp4"
output_video_path = "test_videos/Karlos.mp4"
output_audio_path = "test_videos/adam.wav"
audio_clip = AudioFileClip("test_videos/adam.wav")

transcriber = VideoTranscriber(model_path, video_path)
transcriber.extract_audio()
transcriber.transcribe_video()
transcriber.create_video(output_video_path,audio_clip.duration,background_music_path="test_videos\WiiMusic.mp3")
'''