import streamlit as st
import os
# Assuming story_generator.py and tts.py are in the same directory
from story_generator import generate_story
from tts import text_to_speech

# --- App Title and Header ---
st.set_page_config(page_title="StoryTeller AI", layout="centered")
st.title("✨ StoryTeller AI: Personalized Story Generator ✨")
st.markdown("Enter a prompt and let AI create a short story with voice narration!")

# --- User Input ---
st.header("Your Prompt")
prompt = st.text_area("Tell me about the story you want to generate:", height=100, help="E.g., A futuristic detective solving a case on Mars, A talking animal going on an adventure.")
print(prompt)
# --- Generate Button ---
if st.button("Generate Story & Narration"):
    if not prompt:
        st.warning("Please enter a prompt!")
        print( "prompt entered")
    else:
        # --- Story Generation ---
        with st.spinner("Generating story..."):
            print("generating story")
            generated_story = generate_story(prompt)

        if generated_story and "error occurred" not in generated_story.lower(): # Check if generation was successful
            st.header("Generated Story")
            print("story generated")
            st.write(generated_story)

            # --- Text-to-Speech ---
            st.header("Story Narration")
            # Define a temporary filename for the audio
            audio_filename = f"story_{hash(generated_story)}.mp3" # Use hash for unique filename

            with st.spinner("Generating audio narration..."):
                audio_file_path = text_to_speech(generated_story, filename=audio_filename)

            if audio_file_path and os.path.exists(audio_file_path):
                # --- Audio Playback ---
                try:
                    with open(audio_file_path, 'rb') as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format='audio/mp3')

                    # --- Download Buttons ---
                    st.download_button(
                        label="Download Story (Text)",
                        data=generated_story,
                        file_name="generated_story.txt",
                        mime="text/plain"
                    )
                    st.download_button(
                        label="Download Story (Audio)",
                        data=audio_bytes,
                        file_name="story_narration.mp3", # You can use a fixed name for download
                        mime="audio/mp3"
                    )
                except Exception as e:
                     st.error(f"Could not load or play audio file: {e}")
                     st.info("Audio file might have been generated but could not be loaded for playback/download.")

                # Clean up the temporary audio file after display/download options are provided
                # Note: Streamlit reruns the script, so cleanup needs careful handling if you wanted to automate it.
                # For simplicity here, the files will persist until the script environment is reset or manual cleanup.
                # You could add os.remove(audio_file_path) here, but be mindful of Streamlit's execution model.
                # A more robust app might manage temp files differently.
            else:
                st.error("Failed to generate audio narration.")
        elif "error occurred" in generated_story.lower():
             st.error(generated_story) # Display error from generator
        else:
            st.error("Story generation failed.")


# --- Footer ---
st.markdown("---")
st.markdown("Created for your personalized storytelling experience.")
