"""
quasiword v0.8 WIP
 - Complete rewrite (again, lmao)
"""

import ngram
import wordlist_utils as wl
import pickle
from os.path import exists

MODEL_FILENAME = 'quasiword.ngm'
GRAMS = 7

ngm = ngram.NGramModel(GRAMS)


def init():
    # Import file if it exists
    if exists(MODEL_FILENAME):
        ngm.load_dataset_from_file(MODEL_FILENAME)
    # If not, create a blank file
    else:
        ngm.save_dataset_to_file(MODEL_FILENAME)


def reset():
    # Reset all tensors in model
    ngm.N = {}
    ngm.P = {}
    ngm.B = {}
    # Wipe saved model file
    ngm.save_dataset_to_file(MODEL_FILENAME)


def learn_wordlist_file(filename: str):
    # Learn all words in a file
    wordlist = wl.fr_import_wordlist(filename)
    wordlist = wl.remove_illegal_strs(wordlist)
    ngm.learn_words(wordlist)
    ngm.save_dataset_to_file(MODEL_FILENAME)


def learn_wordlist_files(filenames: [str]):
    # Learn all words in multiple files
    for filename in filenames:
        wordlist = wl.fr_import_wordlist(filename)
        ngm.learn_words(wordlist)
    ngm.save_dataset_to_file(MODEL_FILENAME)


def autolearn(gamma=ngram.DEFAULT_GAMMA):
    print('quasiword: Autolearning...')
    for i in range(3, GRAMS+1):  # Generate words of all lengths from 3 to grams + 1
        print(f'quasiword: Autolearning {i}-character words...')
        wordlist = ngm.exhaustive_list(i, i, gamma=gamma)  # Generate words of given length and gamma
        if i < 6:  # Remove illegal words - testing showed only length 3-5 generates illegal words
            print(f'quasiword: Removing illegal words...')
            word_count = len(wordlist)
            wordlist = wl.remove_illegal_strs(wordlist)
            illegal_count = word_count - len(wordlist)
            print(f'quasiword: Removed {illegal_count} illegal words.')
        ngm.learn_words(wordlist)  # Learn the generated words
    print('quasiword: Done autolearning.')
    ngm.save_dataset_to_file(MODEL_FILENAME)  # Save model to file


# Primary function - uses ngram model to generate a wordlist file full of quasiwords
def generate_wordlist(min_length=3, max_length=16, gamma=ngram.DEFAULT_GAMMA):
    filename = f'quasiwords_{min_length}-{max_length}-{gamma}.txt'
    wordlist = ngm.exhaustive_list(min_length, max_length, gamma)  # Generate list
    if min_length < 6:  # Remove illegal words - testing showed only length 3-5 generates illegal words
        print('quasiword: Removing illegal words...')
        word_count = len(wordlist)
        wordlist = wl.remove_illegal_strs(wordlist)
        illegal_count = word_count - len(wordlist)
        print(f'quasiword: Removed {illegal_count} illegal words.')
    wl.fw_export_wordlist(filename, wordlist)  # Save model to file
    return len(wordlist)
