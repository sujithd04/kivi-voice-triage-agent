"""
create_test_audio.py
Generates 4 test voice feedback WAV files for the Kivi triage demo.
"""

import os
import wave
import struct
import math

FEEDBACK_SAMPLES = [
    ("feedback_1.wav", "Kivi mein login karte hi app crash ho jaata hai"),
    ("feedback_2.wav", "Yaar app open karte time crash ho raha hai, login ke baad"),
    ("feedback_3.wav", "Voice reply bahut slow aata hai"),
    ("feedback_4.wav", "Dark mode ka option add karo please"),
]

def generate_sapi_audio(filename: str, text: str):
    """Generate audio using Windows SAPI if available."""
    try:
        import win32com.client
        voice = win32com.client.Dispatch("SAPI.SpVoice")
        file_stream = win32com.client.Dispatch("SAPI.SpFileStream")
        # 3 is SSFMCreateForWrite
        file_stream.Open(filename, 3, False)
        voice.AudioOutputStream = file_stream
        voice.Speak(text)
        file_stream.Close()
        return True
    except Exception as e:
        print(f"SAPI voice generation failed for {filename}: {e}")
        return False

def generate_fallback_wav(filename: str, duration_sec: float = 2.0):
    """Generate a clean synthetic WAV file if SAPI is unavailable."""
    sample_rate = 16000
    num_samples = int(sample_rate * duration_sec)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        for i in range(num_samples):
            # Gentle synthetic acoustic pattern
            t = float(i) / sample_rate
            value = int(32767.0 * 0.2 * math.sin(2.0 * math.pi * 440.0 * t))
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)

def main():
    print("Generating 4 test audio files...")
    for filename, text in FEEDBACK_SAMPLES:
        success = generate_sapi_audio(filename, text)
        if not success:
            generate_fallback_wav(filename)
            print(f"[Fallback WAV] Created {filename} ({text})")
        else:
            print(f"[Generated] {filename}: \"{text}\"")

    # Clean up test.wav if it exists
    if os.path.exists("test.wav"):
        try:
            os.remove("test.wav")
        except OSError:
            pass

    print("\nAll 4 test audio recordings are ready in the kivi-agent directory!")

if __name__ == "__main__":
    main()
