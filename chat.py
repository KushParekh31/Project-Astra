import json
import random
import torch

from astra.models.neural_net import NeuralNet
from astra.core.tokenizer import bag_of_words, tokenize
from astra.core.memory import learn, recall
from astra.core.knowledge import (
    learn_sentence,
    find_best_match
)
from astra.curiosity.engine import find_topic

device = torch.device("cpu")

# Load intents
with open("data/intents.json", "r") as json_data:
    intents = json.load(json_data)

# Load trained model
FILE = "model.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]

all_words = data["all_words"]
tags = data["tags"]

model_state = data["model_state"]

model = NeuralNet(
    input_size,
    hidden_size,
    output_size
).to(device)

model.load_state_dict(model_state)
model.eval()

bot_name = "Astra"

print(f"{bot_name}: Hello! Type 'quit' to exit.")

while True:

    sentence = input("You: ").strip()

    # =========================
    # EXIT
    # =========================

    if sentence.lower() == "quit":

        print(
            f"{bot_name}: Goodbye!"
        )

        break

    # =========================
    # KEY-VALUE LEARNING
    # =========================

    if sentence.lower().startswith("learn:"):

        try:

            data = sentence[6:].strip()

            key, value = data.split(
                "=",
                1
            )

            key = key.strip()
            value = value.strip()

            learn(
                key,
                value
            )

            print(
                f"{bot_name}: Learned '{key}'."
            )

        except ValueError:

            print(
                f"{bot_name}: Use format -> "
                "learn: key = value"
            )

        continue

    # =========================
    # SENTENCE LEARNING
    # =========================

    if sentence.lower().startswith(
        "learn sentence:"
    ):

        fact = sentence[
            len("learn sentence:")
        :].strip()

        learn_sentence(fact)

        print(
            f"{bot_name}: Learned."
        )

        continue

    # =========================
    # MEMORY LOOKUP
    # =========================

    if sentence.lower().startswith(
        "what is"
    ):

        key = (
            sentence.lower()
            .replace(
                "what is",
                ""
            )
            .replace(
                "?",
                ""
            )
            .strip()
        )

        answer = recall(key)

        if answer:

            print(
                f"{bot_name}: {answer}"
            )

            continue

    # =========================
    # KNOWLEDGE BASE SEARCH
    # =========================

    answer = find_best_match(
        sentence
    )

    if answer:

        print(
            f"{bot_name}: {answer}"
        )

        continue

    # =========================
    # CURIOSITY GRAPH SEARCH
    # =========================

    topic_data = find_topic(
        sentence
    )

    if topic_data:

        print()

        print(
            f"{bot_name}:"
        )

        print(
            topic_data["summary"]
        )

        continue

    # =========================
    # AI PREDICTION
    # =========================

    tokenized_sentence = tokenize(
        sentence
    )

    X = bag_of_words(
        tokenized_sentence,
        all_words
    )

    X = X.reshape(
        1,
        X.shape[0]
    )

    X = torch.from_numpy(
        X
    ).to(device)

    output = model(X)

    _, predicted = torch.max(
        output,
        dim=1
    )

    tag = tags[
        predicted.item()
    ]

    probs = torch.softmax(
        output,
        dim=1
    )

    prob = probs[0][
        predicted.item()
    ]

    if prob.item() > 0.75:

        for intent in intents[
            "intents"
        ]:

            if tag == intent[
                "tag"
            ]:

                print(
                    f"{bot_name}: "
                    f"{random.choice(intent['responses'])}"
                )

                break

    else:

        print(
            f"{bot_name}: "
            "I don't know that yet."
        )
