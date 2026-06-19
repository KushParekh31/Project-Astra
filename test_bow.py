from astra.tokenizer import *

sentence = ["hello"]

words = [
    "hello",
    "bye",
    "thanks"
]

print(
    bag_of_words(
        sentence,
        words
    )
)