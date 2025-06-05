# StoryTeller AI: Personalized Story Generator with Voice Narration

## Project Description

This project, **StoryTeller AI**, is a personalized story generator designed to create short, creative stories based on user-provided prompts and provide accompanying voice narration. It leverages the power of a fine-tuned language model to generate text and a text-to-speech engine for audio output. The entire system is presented through an interactive web-based graphical user interface (GUI) built with Streamlit.

The core AI component is a **GPT-2 small language model** from HuggingFace Transformers, which has been fine-tuned on a curated dataset including creative writing prompts from the **r/WritingPrompts Dataset (Kaggle)**, as well as additional short stories from **Open Library and Fairy Tale Datasets** to enhance genre diversity.

Users interact with the system by entering a **custom natural language prompt** via the Streamlit GUI. This prompt is fed to the fine-tuned GPT-2 model, which then generates an **original short story (typically 100-200 words)** based on the prompt and the patterns learned during fine-tuning.

Immediately following the story generation, the text is passed to a **Text-to-Speech (TTS) engine** (using `gtts`) to create an **audio version** of the narration. Both the generated story text and its audio narration are then displayed within the Streamlit application, where users can **listen to the story** and **download** both the text and the audio files.

The project demonstrates multimodal integration by combining text generation and audio output within a user-friendly interface, aiming to provide a creative and accessible storytelling experience.
![PHOTO-2025-05-29-20-18-18](https://github.com/user-attachments/assets/9f7ac7b2-b137-4c32-a62c-f714468a83b8)
![PHOTO-2025-05-29-20-18-40](https://github.com/user-attachments/assets/86484d65-4b0c-4cb6-a13f-7a40942241a2)


## Features

- Generates short stories based on user prompts.
- Provides audio narration for each generated story.
- Interactive web GUI using Streamlit.
- Option to download generated stories (text and audio).

## Setup and Installation

1.  **Clone the repository (if applicable):**

    ```bash
    # If your project is in a git repository
    git clone <your_repo_url>
    cd <your_project_directory>
    ```

2.  **Create a Conda Environment (Recommended):**

    ```bash
    conda create -n storyteller_env python=3.10
    conda activate storyteller_env
    ```
    *(Replace `storyteller_env` with your desired environment name and `3.10` with a compatible Python version, e.g., 3.8, 3.9, 3.10, 3.11)*

3.  **Install Dependencies:**

    Install the required Python packages using the provided `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

    *Note: If you plan to train the model on a GPU, ensure that the PyTorch version installed by pip is a CUDA-enabled version compatible with your system's CUDA drivers.* For example, you might need to use a command like `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118` after activating your environment, replacing `cu118` with your CUDA version.

## Data Preparation

Prepare your training data in a text file (e.g., `writing_prompts.txt`) where each example is formatted as:

```
Prompt: <prompt>\nStory: <story>\n\n
```

Ensure this file is accessible from the project's main directory.

## Model Fine-Tuning

To fine-tune the GPT-2 model on your dataset, use the `finetune_gpt2.py` script. This is typically done on a computing cluster like Quest for GPU acceleration.

Adjust the parameters in the `finetune.sh` (or your Slurm script) and run it:

```bash
# Example Slurm script submission (adjust script name as needed)
sbatch finetune.sh
```

The fine-tuned model will be saved to the directory specified in your Slurm script (`output_dir`). Make sure the `FINE_TUNED_MODEL_PATH` variable in `story_generator.py` points to this saved model.

## Running the Application

1.  **Activate your environment:**

    ```bash
    conda activate <your_environment_name>
    ```

2.  **Navigate to the project directory:**

    ```bash
    cd /path/to/your/GENAI_2
    ```

3.  **Run the Streamlit app:**

    ```bash
    streamlit run app.py
    ```

    The application will open in your web browser.

## Project Structure

```
GENAI_2/
├── app.py          # Streamlit web application
├── finetune_gpt2.py # Script for fine-tuning GPT-2
├── finetune.sh     # Example Slurm batch script for training on Quest
├── story_generator.py # Script for generating stories using the fine-tuned model
├── tts.py          # Script for text-to-speech conversion
├── requirements.txt # Project dependencies
├── README.md       # Project documentation
└── writing_prompts.txt # Your training data (example filename)
└── logs/           # Directory for training logs and saved models
    └── GPT2_Finetuning_Run1/ # Example run directory
        └── finetuned_model/ # Saved fine-tuned model
```

## Customization and Further Development

- **Dataset:** Experiment with different datasets to influence the story style.
- **Model:** Try fine-tuning larger GPT-2 models or other language models.
- **Generation Parameters:** Adjust `max_length`, `temperature`, `top_k`, `top_p` in `story_generator.py` for different generation behaviors.
- **TTS:** Explore different TTS libraries or voices.
- **GUI:** Enhance the Streamlit interface with more features or a different design.

