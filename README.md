# 🎥 Auto-YouTube-Shorts-Maker

## Overview  
**Auto-YouTube-Shorts-Maker** is a Python-based automation tool designed to create YouTube Shorts by retrieving random jokes from the **r/Jokes** subreddit and generating videos where an AI, powered by **ElevenLabs**, narrates the jokes.

Additionally, this script supports **automated uploads to an AWS server**, which schedules video uploads every **8 hours**, allowing full automation of the content creation process.

---

## Features  
- ✅ **Automated Joke Retrieval** – Fetches random jokes from the **r/Jokes** subreddit.  
- ✅ **AI Voice Narration** – Uses **ElevenLabs** to generate high-quality AI voiceovers.  
-  **Dynamic Background Videos** – Supports gameplay or any long video as a background. It selects **random segments**, enabling unique shorts from a single video source. It also adds music background if you want. 
- ✅ **Auto-subtitle generation** - Automatically detects words and generates subtitles on the screen for better engagement for the video.
- ✅ **Duplicate Detection** – Ensures that the same joke is not used in multiple videos.  
- ✅ **AWS Auto Uploading** – Automatically transfers generated videos to an AWS server, which you can setup for scheduling uploads every X hours/days/minutes you want.  

---

## How It Works  
1. **Fetch a Joke** – The script retrieves a random joke from **r/Jokes**.  
2. **Generate AI Narration** – The joke is converted into speech using **ElevenLabs**.  
3. **Select a Background Video** – A random portion of a pre-existing long video (gameplay, stock footage, etc.) is selected.  
4. **Create the YouTube Short** – The video is rendered with the AI-narrated joke.  
5. **Upload to AWS** – The script automatically uploads the video to an AWS server, which then schedules it for YouTube every 8 hours.  
6. **Check for Duplicates** – Before creating a new video, it verifies whether the joke has already been used.  

---

## Installation & Setup  

### Prerequisites  
Ensure you have the following installed:  
- Python 3.x  
- Required dependencies (install using `pip`)  

### Installation  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-repo/Auto-YouTube-Shorts-Maker.git
   cd Auto-YouTube-Shorts-Maker
2. Install requirements.txt:  
   ```bash
   pip install -r requirements.txt
2. Run shorts.py:  
   ```bash
   python shorts.py

**If you encounter any errors regarding path files and configs just edit the scripts according to your own file paths (API keys of reddit,elevenLabs,AWS e.t.c).**
