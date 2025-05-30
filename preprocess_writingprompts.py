"""
Preprocess Reddit WritingPrompts Dataset (.wp_source/.wp_target) for GPT-2 Fine-Tuning

Usage:
    python preprocess_writingprompts.py --source_file train.wp_source --target_file train.wp_target --output_txt writing_prompts.txt

- Prompts are in .wp_source, stories in .wp_target (same line number = pair)
- Writes each pair as:
    Prompt: <prompt>\nStory: <story>\n\n
This format is suitable for language model fine-tuning.
"""

import argparse

parser = argparse.ArgumentParser(description="Preprocess WritingPrompts .wp_source/.wp_target for GPT-2 fine-tuning.")
parser.add_argument('--source_file', type=str, required=True, help='Path to the .wp_source file (prompts)')
parser.add_argument('--target_file', type=str, required=True, help='Path to the .wp_target file (stories)')
parser.add_argument('--output_txt', type=str, required=True, help='Path to the output text file')
args = parser.parse_args()

def preprocess(source_file, target_file, output_txt):
    count = 0
    with open(source_file, 'r', encoding='utf-8') as src, \
         open(target_file, 'r', encoding='utf-8') as tgt, \
         open(output_txt, 'w', encoding='utf-8') as out:
        for prompt, story in zip(src, tgt):
            prompt = prompt.strip()
            story = story.strip()
            if prompt and story:
                out.write(f"Prompt: {prompt}\nStory: {story}\n\n")
                count += 1
    print(f"Wrote {count} prompt-story pairs to {output_txt}")

if __name__ == "__main__":
    preprocess(args.source_file, args.target_file, args.output_txt) 