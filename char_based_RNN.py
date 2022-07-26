#!/usr/bin/python3.9
#-*- coding: utf-8 -*-

import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

with open("corpus/all.txt") as in_f:
    lovecraft_text = in_f.read()

tokenizer = keras.preprocessing.text.Tokenizer(char_level=True)
tokenizer.fit_on_texts(lovecraft_text)

max_id = len(tokenizer.word_index) # number of distinct characters
dataset_size = tokenizer.document_count # total number of characters

[encoded] = np.array(tokenizer.texts_to_sequences([lovecraft_text])) - 1
train_size = dataset_size * 90 // 100
dataset = tf.data.Dataset.from_tensor_slices(encoded[:train_size])

n_steps = 100
window_length = n_steps + 1 # target = input shifted 1 character ahead
dataset = dataset.window(window_length, shift=1, drop_remainder=True)

dataset = dataset.flat_map(lambda window: window.batch(window_length))

np.random.seed(42)
tf.random.set_seed(42)

batch_size = 32
dataset = dataset.shuffle(10000).batch(batch_size)
dataset = dataset.map(lambda windows: (windows[:, :-1], windows[:, 1:]))

dataset = dataset.map(
        lambda X_batch, Y_batch: (tf.one_hot(X_batch, depth=max_id), Y_batch))

model = keras.models.Sequential([
        keras.layers.GRU(128, return_sequences=True, input_shape=[None, max_id],
            dropout=0.2),
        keras.layers.GRU(128, return_sequences=True,
            dropout=0.2),
        keras.layers.TimeDistributed(keras.layers.Dense(max_id,
                                                        activation="softmax"))
                ])
model.compile(loss="sparse_categorical_crossentropy", optimizer="adam")
history = model.fit(dataset, epochs=10)

model.save("/home/ricky/Documents/code/lovecraft/lcrnn.h5")

def preprocess(texts):
    X = np.array(tokenizer.texts_to_sequences(texts)) - 1
    return tf.one_hot(X, max_id)

X_new = preprocess(["How are yo"])
#Y_pred = model.predict_classes(X_new)
Y_pred = np.argmax(model(X_new), axis=-1)
tokenizer.sequences_to_texts(Y_pred + 1)[0][-1] # 1st sentence, last char

def next_char(text, temperature=1):
    X_new = preprocess([text])
    y_proba = model(X_new)[0, -1:, :]
    rescaled_logits = tf.math.log(y_proba) / temperature
    char_id = tf.random.categorical(rescaled_logits, num_samples=1) + 1
    return tokenizer.sequences_to_texts(char_id.numpy())[0]

def complete_text(text, n_chars=50, temperature=1):
    for _ in range(n_chars):
        text += next_char(text, temperature)
    return text

print(complete_text("t", temperature=1))
