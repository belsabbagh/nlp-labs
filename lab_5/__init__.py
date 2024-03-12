import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
import pickle
import numpy as np

FILE_PATH = "lab_5/blue_castle.txt"

with open(FILE_PATH, "r", encoding="utf8") as f:
    lines = f.readlines()

data = ""
for i in lines:
    data = " ".join(lines)

data = (
    data.replace("\n", "")
    .replace("\r", "")
    .replace("\ufeff", "")
    .replace("“", "")
    .replace("”", "")
)

tokenizer = Tokenizer()
tokenizer.fit_on_texts([data])

pickle.dump(tokenizer, open("token.pkl", "wb"))

sequence_data = tokenizer.texts_to_sequences([data])[0]

vocab_size = len(tokenizer.word_index) + 1

sequences = []
for i in range(3, len(sequence_data)):
    words = sequence_data[i - 3 : i + 1]
    sequences.append(words)

sequences = np.array(sequences)

X = []
y = []

for i in sequences:
    X.append(i[0:3])
    y.append(i[3])

X = np.array(X)
y = np.array(y)

y = to_categorical(y, num_classes=vocab_size)

model = Sequential()
model.add(Embedding(vocab_size, 10, input_length=3))
model.add(LSTM(1000, return_sequences=True))
model.add(LSTM(1000))
model.add(Dense(1000, activation="relu"))
model.add(Dense(vocab_size, activation="softmax"))

model.compile(loss="categorical_crossentropy", optimizer=Adam(learning_rate=0.001))

checkpoint = ModelCheckpoint(
    "next_word.h5", monitor="loss", verbose=1, save_best_only=True
)

model.fit(X, y, epochs=20, batch_size=64, callbacks=[checkpoint])


model = load_model("next_word.h5")
tokenizer = pickle.load(open("token.pkl", "rb"))


def Predict_Next_Words(model, tokenizer, text):
    sequence = tokenizer.texts_to_sequences([text])
    sequence = np.array(sequence)
    preds = np.argmax(model.predict(sequence))
    predicted_word = ""

    for key, value in tokenizer.word_index.items():
        if value == preds:
            predicted_word = key
            break

    print(predicted_word)
    return predicted_word

if __name__ == "__main__":
    while True:
        text = input("Enter your line:")

        if text == "0":
            print("Execution completed....")
            break

        else:
            try:
                text = text.split(" ")
                text = text[-3:]

                Predict_Next_Words(model, tokenizer, text)

            except Exception as e:
                print("Error occurred: ", e)
                continue
