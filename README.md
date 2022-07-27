# lovecraft 

## A Recurrent Neural Network built with Tensorflow - generates H.P. Lovecraft-ian text using a model trained on the British horror author's corpus

##Details about the scripts/notebooks 

`scrape.py` script grabs corpus (105
fiction titles) from: [https://hplovecraft.com](hplovecraft.com) - thank you!

[lovecraft_charRNN_colab.ipynb](https://github.com/emgullufsen/lovecraft/blob/main/lovecraft_charRNN_colab.ipynb)
is the notebook that I ran on google colab cloud platform, to format the data
(corpus) and train the model. This script then saves the model in .h5 format.

`generate_char_based.py` script uses the trained model (loaded from .h5 format),
to generate text.

This Character-based Recurrent Neural Network is based on ideas and code from:
"Hands-on Machine Learning with Scikit-Learn, Keras & Tensorflow", by Aurélien
Géron
