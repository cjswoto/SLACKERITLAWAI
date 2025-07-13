from pathlib import Path

from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset, Dataset


def fine_tune(model_name: str, data_path: Path, output_dir: Path):
    ds = load_dataset('text', data_files=str(data_path))['train']
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    def tokenize(batch):
        tokens = tokenizer(batch['text'], truncation=True, padding='max_length', max_length=128)
        batch['input_ids'] = tokens['input_ids']
        batch['attention_mask'] = tokens['attention_mask']
        return batch

    tokenized = ds.map(tokenize, batched=True)

    args = TrainingArguments(
        output_dir=str(output_dir),
        overwrite_output_dir=True,
        per_device_train_batch_size=1,
        num_train_epochs=1,
    )

    trainer = Trainer(model=model, args=args, train_dataset=tokenized)
    trainer.train()
    trainer.save_model(str(output_dir))
