import json
from pathlib import Path
import subprocess
import tkinter as tk
from tkinter import filedialog, scrolledtext
import ttkbootstrap as tb
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import load_dataset

SLACKER_BLUE = '#66ccff'
MIDNIGHT_BLACK = '#0A0A0A'
FONT_FAMILY = 'Montserrat'
LOG_ENABLED = False

def log_debug(msg: str):
    if LOG_ENABLED:
        Path('logs').mkdir(exist_ok=True)
        with open('logs/debug.txt', 'a') as f:
            f.write(f"{msg}\n")


def validate_dataset(path: Path) -> bool:
    if path.suffix not in {'.jsonl', '.json', '.txt'}:
        return False
    if path.suffix == '.txt':
        return True
    try:
        data = [json.loads(line) for line in path.read_text().splitlines()] if path.suffix == '.jsonl' else json.loads(path.read_text())
        if isinstance(data, dict):
            data = data.get('data', data)
        sample = data[0] if data else {}
        return 'text' in sample
    except Exception:
        return False


class TrainerGUI(tb.Window):
    def __init__(self):
        super().__init__(themename='darkly')
        self.title('Slacker IT Trainer 🦥')
        self.geometry('900x600')
        self.configure(bg=MIDNIGHT_BLACK)
        self.dataset_path: Path | None = None
        self.model_var = tk.StringVar(value='gpt2')
        self.batch_size = tk.IntVar(value=4)
        self.epochs = tk.IntVar(value=3)
        self.lr = tk.StringVar(value='0.0002')
        self.max_len = tk.IntVar(value=512)
        self.lora = tk.BooleanVar()
        self.quant = tk.BooleanVar()
        self._build_ui()

    def _build_ui(self):
        top = tb.Label(self, text='Slacker IT Trainer 🦥', font=(FONT_FAMILY, 20, 'bold'), background=MIDNIGHT_BLACK, foreground=SLACKER_BLUE)
        top.pack(pady=10)
        body = tb.Frame(self)
        body.pack(fill='both', expand=True, padx=10)
        left = tb.Frame(body)
        left.pack(side='left', fill='y')
        right = tb.Frame(body)
        right.pack(side='right', fill='both', expand=True)
        browse = tb.Button(left, text='Select Dataset', command=self.select_dataset, bootstyle='primary')
        browse.pack(pady=5)
        self.dataset_label = tb.Label(left, text='No file selected', width=30)
        self.dataset_label.pack(pady=5)
        model_box = tb.Combobox(right, values=['gpt2','gpt2-medium','gpt2-large','EleutherAI/gpt-neo-125M'], textvariable=self.model_var)
        model_box.pack(pady=5)
        tb.Label(right, text='Batch Size').pack()
        tb.Scale(right, from_=1, to=32, variable=self.batch_size, orient='horizontal').pack(fill='x')
        tb.Label(right, text='Epochs').pack()
        tb.Combobox(right, values=list(range(1,11)), textvariable=self.epochs).pack()
        tb.Label(right, text='Learning Rate').pack()
        tb.Combobox(right, values=['0.0001','0.0002','0.0005','0.001'], textvariable=self.lr).pack()
        tb.Label(right, text='Max Seq Length').pack()
        tb.Combobox(right, values=[128,256,512,1024], textvariable=self.max_len).pack()
        tb.Checkbutton(right, text='Enable LoRA', variable=self.lora).pack(anchor='w')
        tb.Checkbutton(right, text='4-bit Quantization', variable=self.quant).pack(anchor='w')
        tb.Button(right, text='Fine-Tune Model', command=self.train, bootstyle='success').pack(pady=5)
        tb.Button(right, text='Convert to GGUF', command=self.convert, bootstyle='warning').pack(pady=5)
        self.log = scrolledtext.ScrolledText(self, height=8, font=('Fira Code', 10))
        self.log.pack(fill='x', padx=10, pady=5)

    def log_msg(self, msg: str, color: str='white'):
        self.log.insert('end', msg + '\n')
        self.log.tag_add(color, 'end-1l', 'end-1c')
        self.log.tag_config(color, foreground=color)
        self.log.see('end')
        log_debug(msg)

    def select_dataset(self):
        path = filedialog.askopenfilename(filetypes=[('Data','*.json *.jsonl *.txt')])
        if path:
            p = Path(path)
            if validate_dataset(p):
                self.dataset_path = p
                self.dataset_label.config(text=p.name)
                self.log_msg('🟢 Dataset loaded', 'green')
            else:
                self.log_msg('❌ Invalid dataset', 'red')

    def train(self):
        if not self.dataset_path:
            self.log_msg('❌ Select a dataset first', 'red')
            return
        self.log_msg('⏳ Training...', 'yellow')
        model_name = self.model_var.get()
        output = Path('trained_models')/model_name
        args = TrainingArguments(
            output_dir=str(output),
            per_device_train_batch_size=self.batch_size.get(),
            num_train_epochs=self.epochs.get(),
            learning_rate=float(self.lr.get()),
        )
        ds = load_dataset('json' if self.dataset_path.suffix in {'.jsonl','.json'} else 'text', data_files=str(self.dataset_path))['train']
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

        def tokenize(batch):
            tokens = tokenizer(batch['text'], truncation=True, padding='max_length', max_length=self.max_len.get())
            batch['input_ids'] = tokens['input_ids']
            batch['attention_mask'] = tokens['attention_mask']
            return batch

        tokenized = ds.map(tokenize, batched=True)
        trainer = Trainer(model=model, args=args, train_dataset=tokenized)
        trainer.train()
        trainer.save_model(str(output))
        self.log_msg('🟢 Training complete, nice work!', 'green')

    def convert(self):
        model_name = self.model_var.get()
        src = Path('trained_models')/model_name
        out = Path('gguf_models')/f'{model_name}.gguf'
        out.parent.mkdir(exist_ok=True)
        self.log_msg('⏳ Converting... hang tight', 'yellow')
        try:
            subprocess.run(['python','./llama.cpp/convert.py','--model',str(src),'--outfile',str(out),'--quant','q4_0'], check=True)
            self.log_msg('🟢 Conversion complete', 'green')
        except subprocess.CalledProcessError:
            self.log_msg('❌ Conversion failed', 'red')


def main():
    app = TrainerGUI()
    app.mainloop()


if __name__ == '__main__':
    main()
