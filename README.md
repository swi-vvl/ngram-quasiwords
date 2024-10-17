# ngram-quasiwords
Generates quasiwords with an n-gram language model.

# Technical Report and Overview
This code was written to accomplish a specific goal of increasing the strength of passphrases without compromising pronouncability or ease of typing. A technical report of this project, including a technical overview of how this code works, can be found here:

https://docs.google.com/document/d/1TEtF3rD9nwuw_kjDFOcJKsg0k9EUzHrlEevtbMWBfa0/edit?usp=sharing

# How to use
This code requires numpy and pickle to run. You will need to have both installed in your python environment. Use `pip install numpy` and `pip install pickle` to install both.

To use this code, simply run `main.py`. It is set by default to generate a list of 345,000,000 quasiwords. This file will be 3.33 GB in size. Adjusting the behavior of this program will require manually editing main.py, as it is not yet parameterized.
