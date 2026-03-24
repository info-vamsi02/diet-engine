import os
import pandas as pd
import torch
import pickle

from sklearn.preprocessing import LabelEncoder
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments

# ================= PATH SETUP =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# create folder for model
MODEL_DIR = os.path.join(BASE_DIR, "../saved_model")
os.makedirs(MODEL_DIR, exist_ok=True)

# ================= LOAD DATA =================
csv_path = os.path.join(BASE_DIR, "../diet_recommendations_dataset.csv")

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Dataset not found at {csv_path}")

data = pd.read_csv(csv_path)

# ================= CREATE INPUT TEXT =================
data["text"] = data.apply(
    lambda x: f"Age {x.Age}, Gender {x.Gender}, BMI {x.BMI}, Disease {x.Disease_Type}, Activity {x.Physical_Activity_Level}",
    axis=1
)

# ================= LABEL ENCODING =================
labels = data["Diet_Recommendation"]

le = LabelEncoder()
labels = le.fit_transform(labels)

# save encoder
with open(os.path.join(MODEL_DIR, "label_encoder.pkl"), "wb") as f:
    pickle.dump(le, f)

# ================= TOKENIZER =================
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

encodings = tokenizer(
    list(data["text"]),
    truncation=True,
    padding=True,
    max_length=64
)

# ================= DATASET CLASS =================
class DietDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item

    def __len__(self):
        return len(self.labels)

dataset = DietDataset(encodings, labels)

# ================= MODEL =================
model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=len(set(labels))
)

# ================= TRAINING =================
training_args = TrainingArguments(
    output_dir=os.path.join(BASE_DIR, "../results"),
    num_train_epochs=3,
    per_device_train_batch_size=8,
    logging_dir=os.path.join(BASE_DIR, "logs"),
    save_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

print("🚀 Training started...")
trainer.train()
training_args = TrainingArguments(
    output_dir=os.path.join(BASE_DIR, "../results"),
    num_train_epochs=3,
    per_device_train_batch_size=8,
    logging_dir=os.path.join(BASE_DIR, "logs"),
    logging_steps=10,              # ✅ ADD THIS
    evaluation_strategy="epoch",   # ✅ ADD THIS
    save_strategy="epoch",
    report_to="none"               # avoid warnings
)


# ================= SAVE MODEL =================
model.save_pretrained(MODEL_DIR)
tokenizer.save_pretrained(MODEL_DIR)

print("✅ Model saved in 'saved_model' folder")
