# ngram-quasiwords
Generates quasiwords with an n-gram language model.

# Technical report and overview
This code was written to accomplish a specific goal of increasing the strength of passphrases without compromising pronouncability or ease of typing. A technical report of this project, including a technical overview of how this code works, can be found here:

https://docs.google.com/document/d/1TEtF3rD9nwuw_kjDFOcJKsg0k9EUzHrlEevtbMWBfa0/edit?usp=sharing

# Examples of "quasiwords"
Quasiwords are the name I've given to fake words - technically pronounceable within the phonology rules of english, but still gibberish. There are many orders of magnitude more possible quasiwords than there are actual english words. Here are a few examples:

- Platacil | Janarius | Daboorig | Malstorg | Roghung | Vicepad | Eoberano | Aturads | Ceturlob | Nadapot | Twinex | Wraxanky | Yoineepa | Sokoutin | Krosonox | Hrogrugg | Cohetorb | Azulikid | Fripeye | Ipacudda


# How to use
This code requires numpy and pickle to run. You will need to have both installed in your python environment. Use `pip install numpy` and `pip install pickle` to install both.

To use this code, simply run `main.py`. It is set by default to generate a list of 345,500,000 quasiwords between 3 and 8 letters in length. **This process will take several minutes and the resulting file will be 3.33 GB in size**. Adjusting the behavior of this program will require manually editing main.py, as it is not yet parameterized.

# Overview summary
The TL;DR of how this code works:

- The n-gram model is initialized with grams = 7 with lines 12-14 in `quasiword.py`, corresponding to a maximum context window length of 6 (grams - 1).
- `ngram.learn_words` is called with a list of ~368,000 English words to train with.
- `ngram.learn_words` calls `ngram._slice_and_learn` with each word.
- `ngram._slice_and_learn` slices each word into smaller substrings of lengths from 2 to 6, then calls `ngram._learn` with each slice.
- `ngram._learn` increments counters for each unique slice encountered, storing final counts in the dataset.
- `quasiword.autolearn` is called to train the model on its own output, completing the training process.
- Generation begins by calling `ngram.exhaustive_list` with a minimum word length of 4 and a maximum word length of 8.
- `ngram.exhaustive_list` calls `ngram._recursive_list` once for each word length between 4 and 8, passing in dynamic context lengths of 3 to 6, determined by `ngram.dynamic_context`
- `ngram._recursive_list` calls itself, recursively adding letters one after another to create new words. It does this for all possible combinations of letters across the entire learned dataset.
- A wordlist is returned and written to file, containing 345,500,000 quasiwords.
