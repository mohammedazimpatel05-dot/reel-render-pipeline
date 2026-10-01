import os
from gtts import gTTS
# MoviePy v2.x ke liye updated imports:
from moviepy import TextClip, CompositeVideoClip, ColorClip, AudioFileClip

def create_reel(text, output_filename="output/reel_1.mp4"):
    os.makedirs("assets", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    print("1. Text-to-Speech audio generate ho raha hai...")
    tts = gTTS(text=text, lang="en", slow=False)
    audio_path = "assets/temp_audio.mp3"
    tts.save(audio_path)

    audio = AudioFileClip(audio_path)
    duration = audio.duration

    print("2. Background clip ban rahi hai...")
    background = ColorClip(size=(1080, 1920), color=(15, 23, 42), duration=duration)

    print("3. Text overlay attach ho raha hai...")
    text_clip = TextClip(
        text=text,
        font_size=50,
        color="white",
        size=(900, None),
        method="caption"
    ).with_duration(duration).with_position("center")

    print("4. Video assemble ho rahi hai...")
    video = CompositeVideoClip([background, text_clip])
    video = video.with_audio(audio)

    print("5. Video rendering in progress...")
    video.write_videofile(
        output_filename,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    print(f"DONE! Reel saved at: {output_filename}")

if __name__ == "__main__":
    prompt = "Consistency is the key to building great software projects."
    create_reel(prompt)

