import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Define the path to your fine-tuned model
# This should match the output_dir you used in your finetune.sh script
FINE_TUNED_MODEL_PATH = './logs/GPT2_Finetuning_Run1/finetuned_model' # Adjust if your logs structure is different

# Load the tokenizer and model from the saved directory
try:
    tokenizer = GPT2Tokenizer.from_pretrained(FINE_TUNED_MODEL_PATH)
    model = GPT2LMHeadModel.from_pretrained(FINE_TUNED_MODEL_PATH)
except Exception as e:
    print(f"Error loading fine-tuned model from {FINE_TUNED_MODEL_PATH}: {e}")
    print("Please ensure the path is correct and the model files exist.")
    # Fallback to base GPT-2 if fine-tuned model fails to load (optional)
    # print("Falling back to base gpt2 model.")
    # tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    # model = GPT2LMHeadModel.from_pretrained('gpt2')
    # FINE_TUNED_MODEL_PATH = 'gpt2 (base model fallback)'


# Add a pad token if the tokenizer doesn't have one (needed for generation with padding)
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    model.resize_token_embeddings(len(tokenizer))


def generate_story(prompt, max_length=200, num_return_sequences=1):
    """
    Generates a story based on a given prompt using the fine-tuned GPT-2 model.

    Args:
        prompt (str): The user's input prompt.
        max_length (int): The maximum length of the generated story (including the prompt).
        num_return_sequences (int): The number of sequences to generate.

    Returns:
        str: The generated story text, or an error message if generation fails.
    """
    if not prompt:
        return "Please enter a prompt to generate a story."

    # Format the input text to match the training data format ("Prompt: ... Story:")
    input_text = f"Prompt: {prompt} Story:"

    try:
        # Encode the input text
        input_ids = tokenizer.encode(input_text, return_tensors='pt')

        # Determine the device (CPU or GPU)
        device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        model.to(device)
        input_ids = input_ids.to(device)

        # Generate text
        output = model.generate(
            input_ids,
            max_length=max_length,
            num_return_sequences=num_return_sequences,
            no_repeat_ngram_size=2,
            do_sample=True, # Enable sampling for more creative output
            top_k=40,
            top_p=0.9,
            temperature=0.7,
            # Set pad_token_id to eos_token_id if pad token is not explicitly added
            pad_token_id=tokenizer.eos_token_id if tokenizer.pad_token is None else tokenizer.pad_token_id,
            attention_mask=input_ids.ne(tokenizer.pad_token_id).long().to(device) if tokenizer.pad_token is not None else None, # Add attention mask if padding is used

        )

        # Decode the generated text
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

        # Extract only the story part after "Story:"
        # Split by "Story:" and take the last part, then strip leading/trailing whitespace
        story = generated_text.split("Story:")[-1].strip()

        # Optional: Further clean-up if the model generates repetitive text or includes the prompt again
        if story.startswith("Prompt:"):
             story = story.split("Prompt:")[0].strip()


        return story

    except Exception as e:
        return f"An error occurred during story generation: {e}"

# if __name__ == '__main__':
#     # Example usage (for testing)
#     test_prompt = "A wizard who lost their spellbook"
#     print(f"Generating story for prompt: '{test_prompt}'")
#     generated_story = generate_story(test_prompt)
#     print("\nGenerated Story:")
#     print(generated_story)

#     test_prompt_2 = "The last robot on Earth finds a flower"
#     print(f"\nGenerating story for prompt: '{test_prompt_2}'")
#     generated_story_2 = generate_story(test_prompt_2)
#     print("\nGenerated Story:")
#     print(generated_story_2)
