# lovecraft 

#### A Recurrent Neural Network built with Tensorflow - generates H.P. Lovecraft-ian text using a model trained on the British horror author's corpus

#### Details about the scripts/notebooks: 
`scrape.py` script grabs corpus (105 fiction titles) from: 
[https://hplovecraft.com](hplovecraft.com) - thank you!

[lovecraft_charRNN_colab.ipynb](https://github.com/emgullufsen/lovecraft/blob/main/lovecraft_charRNN_colab.ipynb)
is the notebook that I wrote and ran on google colab cloud platform (my own
NVIDIA GPU at home has only compute ability 5.0, and does not train Gated
Recurrent Unit models nearly as quickly as the GPUs/TPUs on the colab
platform), to format the data (corpus) and train the model. This script then
saves the model in .h5 format.

`generate_char_based.py` script uses the trained model (loaded from .h5
format), to generate text.

This Character-based Recurrent Neural Network is based on ideas and code from:
"Hands-on Machine Learning with Scikit-Learn, Keras & Tensorflow", by Aurélien
Géron

#### IMPORTANT NOTES FOR RUNNING SCRIPTS: 
Invoke with `python3 generate_char_based.py` to generate text the she-bang at
top of my scripts points right to python3.9 - this will likely not work unless
you have that specific version installed. You can of course amend the she-bang
line and invoke directly i.e. `./generate_char_based.py`. For convenience I
have saved the entire corpus (all.txt), and the trained-model in .h5 format, so
one does not need to run the `scrape.py` and `lovecraft_charRNN_colab.ipynb`
scripts prior to running `generate_char_based.py`. Please note there is a
word-based version I tried initially in the `train.py` script. Thanks! -Eric
