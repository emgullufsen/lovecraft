#!/usr/bin/python3.9
#-*- coding: utf-8 -*-
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
import numpy as np 

def clean_sentence(sentence):
	return sentence.replace(",", " , ") \
				   .replace(".", " . ") \
				   .replace("-", " - ") \
				   .replace("\u2014", " \u2014 ") \
				   .replace("/", " / ")

VOCAB_SIZE = 2000
EMBEDDING_DIM = 8
OOV_TOK = "<OOV>"
FILES_LIMIT = 10
max_sequence_len = 6

data = ''

FILES_LIM = 8
c = 0
for filename in os.listdir("corpus"):
    if c >= FILES_LIM:
        break
    c += 1
    with open(os.path.join("corpus", filename), 'r', encoding="UTF-8") as f:
        text = f.read()
        data += text

data = clean_sentence(data)
corpus = data.lower()
alltext = []
alltext.append(corpus)
sentences = []
words = corpus.split(" ")
range_size = len(words)-max_sequence_len
for i in range(0, range_size):
	thissentence=""
	for word in range(0, max_sequence_len-1):
		word = words[i+word]
		thissentence = thissentence + word
		thissentence = thissentence + " "
	sentences.append(thissentence)

tokenizer = Tokenizer(oov_token=OOV_TOK, split=" ", char_level=False)
tokenizer.fit_on_texts(alltext)
total_words = len(tokenizer.word_index) + 1

print(tokenizer.word_index)
print(total_words)

input_sequences = []
for line in sentences:
	token_list = tokenizer.texts_to_sequences([line])[0]
	for i in range(1, len(token_list)):
		n_gram_sequence = token_list[:i+1]
		input_sequences.append(n_gram_sequence)

# pad sequences 
#max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

# create predictors and label
xs, labels = input_sequences[:,:-1],input_sequences[:,-1]

ys = tf.keras.utils.to_categorical(labels, num_classes=total_words)

model = Sequential()
model.add(Embedding(total_words, 16, input_length=max_sequence_len-1))
model.add(Bidirectional(LSTM(32, return_sequences='True')))
model.add(Bidirectional(LSTM(32)))
model.add(Dense(total_words, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(xs, ys, epochs=100, verbose=1)

model.save("/home/ricky/Documents/code/lovecraft/l.h5")

seed_text = "what i saw in the garden was"
next_words = 100

for _ in range(next_words):
	token_list = tokenizer.texts_to_sequences([seed_text])[0]
	token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
	predicted = np.argmax(model.predict(token_list), axis=-1)
	output_word = ""
	for word, index in tokenizer.word_index.items():
		if index == predicted:
			output_word = word
			break
	seed_text += " " + output_word
print(seed_text)
