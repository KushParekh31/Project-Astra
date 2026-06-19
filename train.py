import json
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from astra.tokenizer import tokenize, stem, bag_of_words
from astra.model import NeuralNet

# Load intents
with open("data/intents.json", "r") as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []

# Process patterns
for intent in intents["intents"]:
    tag = intent["tag"]
    tags.append(tag)

    for pattern in intent["patterns"]:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

ignore_words = ["?", ".", "!", ","]

all_words = [
    stem(word)
    for word in all_words
    if word not in ignore_words
]

all_words = sorted(set(all_words))
tags = sorted(set(tags))

# Training data
X_train = []
Y_train = []

for (pattern_sentence, tag) in xy:

    bag = bag_of_words(
        pattern_sentence,
        all_words
    )

    X_train.append(bag)

    label = tags.index(tag)
    Y_train.append(label)

X_train = np.array(X_train)
Y_train = np.array(Y_train)

# Dataset class
class ChatDataset(Dataset):

    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = Y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples


dataset = ChatDataset()

batch_size = 8
hidden_size = 8
input_size = len(X_train[0])
output_size = len(tags)

train_loader = DataLoader(
    dataset=dataset,
    batch_size=batch_size,
    shuffle=True,
    num_workers=0
)

device = torch.device("cpu")

model = NeuralNet(
    input_size,
    hidden_size,
    output_size
).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

epochs = 1000

for epoch in range(epochs):

    for words, labels in train_loader:

        words = words.to(device)
        labels = labels.to(
            dtype=torch.long
        ).to(device)

        outputs = model(words)

        loss = criterion(
            outputs,
            labels
        )

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(
            f"Epoch [{epoch+1}/{epochs}] "
            f"Loss: {loss.item():.4f}"
        )

print("Training complete!")

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags
}

FILE = "model.pth"

torch.save(data, FILE)

print(f"Model saved to {FILE}")
