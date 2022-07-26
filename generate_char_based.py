#!/usr/bin/python3.9
#-*- coding: utf-8 -*-

import os
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np 

np.random.seed(42)
tf.random.set_seed(42)

with open("corpus/all.txt") as in_f:
    lovecraft_text = in_f.read()

model = tf.keras.models.load_model("lovecraft_charRNN.h5")
tokenizer = tf.keras.preprocessing.text.Tokenizer(char_level=True)
tokenizer.fit_on_texts(lovecraft_text)
max_id = len(tokenizer.word_index) # number of distinct characters

def preprocess(texts):
    X = np.array(tokenizer.texts_to_sequences(texts)) - 1
    return tf.one_hot(X, max_id)

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

print(complete_text("i", temperature=1))