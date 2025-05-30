import os
from gtts import gTTS
from pydub import AudioSegment

def text_to_speech(text, filename='story_narration.mp3'):
    """
    Converts text to speech and saves it as an MP3 file.

    Args:
        text (str): The text to convert to speech.
        filename (str): The name for the output MP3 file.

    Returns:
        str: The path to the saved audio file, or None if conversion fails.
    """
    if not text:
        print("Warning: No text provided for text-to-speech.")
        return None

    try:
        # Create gTTS object
        tts = gTTS(text=text, lang='en', slow=False) # lang='en' for English, slow=False for normal speed

        # Save the audio file
        tts.save(filename)
        print(f"Text-to-speech audio saved to {filename}")

        # Optional: Add a small silence at the beginning/end using pydub
        # This can sometimes improve playback in certain players
        # try:
        #     sound = AudioSegment.from_file(filename, format="mp3")
        #     silence = AudioSegment.silent(duration=500) # 500 milliseconds silence
        #     sound = silence + sound + silence
        #     sound.export(filename, format="mp3")
        #     print("Added silence to audio file.")
        # except Exception as e:
        #     print(f"Warning: Could not add silence to audio file: {e}")

        return filename

    except Exception as e:
        print(f"Error during text-to-speech conversion: {e}")
        return None

if __name__ == '__main__':
    # Example usage (for testing)
    test_text = "This is a test sentence to convert to speech."
    print(f"Converting text to speech: '{test_text}'")
    audio_file_path = text_to_speech(test_text, filename="test_output.mp3")

    if audio_file_path:
        print(f"Test audio saved successfully to {audio_file_path}")
        # Note: Playing audio requires a player, which is not standard in a terminal.
        # You would typically play this in the GUI or download it.
        # For command line testing, you might use a player like 'mpg123' if available:
        # os.system(f"mpg123 {audio_file_path}")
    else:
        print("Text-to-speech conversion failed.")
