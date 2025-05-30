"""
Fine-tune GPT-2 on writing_prompts.txt for creative story generation

Usage:
    python finetune_gpt2.py --train_file writing_prompts.txt --output_dir ./gpt2-wp-finetuned

- Expects writing_prompts.txt in the format:
    Prompt: <prompt>\nStory: <story>\n\n
- Saves the fine-tuned model and tokenizer to output_dir
"""

import argparse
from transformers import GPT2Tokenizer, GPT2LMHeadModel, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

parser = argparse.ArgumentParser(description="Fine-tune GPT-2 on writing prompts dataset.")
parser.add_argument('--train_file', type=str, required=True, help='Path to the training text file (writing_prompts.txt)')
parser.add_argument('--output_dir', type=str, required=True, help='Directory to save the fine-tuned model')
parser.add_argument('--epochs', type=int, default=1, help='Number of training epochs (default: 1)')
args = parser.parse_args()

model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

def load_dataset(file_path, tokenizer, block_size=512):
    return TextDataset(
        tokenizer=tokenizer,
        file_path=file_path,
        block_size=block_size
    )

train_dataset = load_dataset(args.train_file, tokenizer)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

training_args = TrainingArguments(
    output_dir=args.output_dir,
    overwrite_output_dir=True,
    num_train_epochs=args.epochs,
    per_device_train_batch_size=1,
    save_steps=5000,
    save_total_limit=2,
    prediction_loss_only=True,
    logging_steps=500,
    report_to="none",
    save_strategy="no",
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

trainer.train()
trainer.save_model(args.output_dir)
tokenizer.save_pretrained(args.output_dir)
print(f"Fine-tuned model and tokenizer saved to {args.output_dir}") 