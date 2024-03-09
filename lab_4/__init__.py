import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

if __name__ == "__main__":
    df = pd.read_csv("data/yelp.csv")

    sentences = df["sentence"]
    labels = df["label"]
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(sentences)
    sequences = tokenizer.texts_to_sequences(sentences)

    max_sequence_length = max(len(seq) for seq in sequences)
    padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length)

    embedding_dim = 16
    vocab_size = len(tokenizer.word_index) + 1

    model = Sequential(
        [
            Embedding(vocab_size, embedding_dim, input_length=max_sequence_length),
            SimpleRNN(32),
            Dense(1, activation="sigmoid"),
        ]
    )

    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    model.fit(padded_sequences, labels, epochs=10, batch_size=2)

    loss, accuracy = model.evaluate(padded_sequences, labels)
    print("Test Loss:", loss)
    print("Test Accuracy:", accuracy)
