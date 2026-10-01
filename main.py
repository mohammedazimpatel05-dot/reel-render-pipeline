import os
from flask import Flask, jsonify, request
from gtts import gTTS
from moviepy import TextClip, CompositeVideoClip, ColorClip, AudioFileClip

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "API is running", "message": "Reel Render Pipeline Operational"})

@app.route('/generate', methods=['POST'])
def generate_reel():
    data = request.get_json() or {}
    prompt = data.get('prompt', 'Consistency is the key to building great software projects')
    
    output_filename = "output/reel_1.mp4"
    os.makedirs("assets", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    tts = gTTS(text=prompt, lang="en", slow=False)
    audio_path = "assets/temp_audio.mp3"
    tts.save(audio_path)

    audio = AudioFileClip(audio_path)
    duration = audio.duration

    background = ColorClip(size=(1080, 1920), color=(15, 23, 42), duration=duration)

    text_clip = (
        TextClip(
            text=prompt,
            font_size=50,
            color="white",
            size=(900, None),
            method="caption"
        )
        .with_duration(duration)
        .with_position("center")
    )

    video = CompositeVideoClip([background, text_clip])
    video = video.with_audio(audio)

    video.write_videofile(
        output_filename,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    return jsonify({
        "status": "success",
        "message": f"Reel generated successfully at {output_filename}"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

