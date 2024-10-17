"""
ngram v0.2 WIP (2024-09-09)
 - Changed N from sparse numpy array to dictionary, reducing memory requirements
"""

import numpy as np
import random
import pickle

DEFAULT_CHARSET = '.abcdefghijklmnopqrstuvwxyz'
DEFAULT_GAMMA = 0.78


class NGramModel:
    def __init__(self, grams: int, charset=DEFAULT_CHARSET):
        self.grams = grams
        # First char in charset taken to be start/end char
        self.charset = charset
        # Enumeration and denumeration tables
        self.stoi = {s: i for i, s in enumerate(charset)}
        self.itos = {i: s for s, i in self.stoi.items()}
        # Dataset N (combination counts), form { str : [uint16] }
        self.N = {}
        # Probability set P, from normalizing the dataset, form { str : [float16] }
        self.P = {}
        # Branch set B, to simplify the process of recursive traversal, form { str : str }
        self.B = {}

    # Generate probability set P from dataset N
    def update_p(self):
        print('ngram: Updating Probabilities...')
        for key in list(self.N.keys()):
            p = np.array(self.N[key], dtype=np.float32)
            p /= sum(p)
            self.P[key] = p
        print('ngram: Probabilities updated.')

    # Generate branch set B from probability set P
    def update_b(self, min_p=0.0):
        print('ngram: Updating Branches...')
        for key in list(self.P.keys()):
            self.B[key] = ''
            for n in range(len(self.charset)):
                if self.P[key][n] > min_p:
                    self.B[key] += self.itos[n]
        print('ngram: Branches updated.')

    # Activation function
    # Modified sin(x) function to be 0 at 0 and 1 at 1
    # beta pulls curve (beta=1.0 is symmetrical around 0.5, 0.5)
    # @staticmethod
    # def sinoid(vec: np.array, beta=1.0):
    #     beta = max(beta, 1e-256)  # Approach but do not equal zero, do not allow non-positive beta
    #     vec = (np.sin(np.pi * (vec - 0.5)) / 2 + 0.5) ** beta
    #     vec /= sum(vec)
    #     return vec

    # Returns context length based on max_length of word; nonlinear
    def dynamic_context(self, max_length, gamma=DEFAULT_GAMMA):
        if max_length == 1:
            return 2
        context = int((max_length - 2) ** gamma + 2)  # always 2 at length 2 and 3 at length 3
        return min(context, self.grams - 1)  # context cannot be larger than grams-1

    # SAVING AND LOADING ==============================================================================================
    def save_dataset_to_file(self, filename):
        print(f'ngram: Saving dataset to file {filename} ...')
        with open(filename, 'wb') as f:
            pickle.dump(self.N, f)  # Use pickle to binary dump the N dataset
        print(f'ngram: Saved to file.')

    def load_dataset_from_file(self, filename):
        print(f'ngram: Loading dataset from file {filename} ...')
        with open(filename, 'rb') as f:
            self.N = pickle.load(f)  # Use pickle to load the N dataset into memory from file
        print(f'ngram: Loaded from file.')
        self.update_p()
        self.update_b()

    # LEARNING ========================================================================================================

    # Add a string to the dataset, using all but the last chars as a key
    def _learn(self, string: str):
        key = string[:-1]  # Use all but the last character as a key
        char = string[-1:]  # Isolate last character
        index = self.stoi[char]  # Enumerate the last character
        if key not in self.N:  # If key doesn't already exist in dataset N, create new key
            self.N[key] = np.zeros(len(self.charset), dtype=np.int32)
        self.N[key][index] += 1  # Add datapoint to dataset N

    # Slice word and _learn each slice
    def _slice_and_learn(self, word: str):
        word = self.charset[0] + word + self.charset[0]  # Add special 'START' and 'END' characters to word
        word_length = len(word)
        max_slice_length = min(self.grams, word_length)  # Enforce maximum context length set by "grams"
        for slice_length in range(2, max_slice_length + 1):  # For slices of various lengths...
            for i in range(word_length - slice_length + 1):  # For each character in the word...
                _slice = word[i:i + slice_length]  # Take a slice
                self._learn(_slice)  # Add the slice to the dataset

    # Learn a list of words
    def learn_words(self, words: [str]):
        print(f'ngram: Learning {len(words)} words ...')
        for word in words:
            self._slice_and_learn(word)
        print(f'ngram: Done learning.')
        self.update_p()  # Generate probability set P
        self.update_b()  # Generate branch set B

    # DATA MANIPULATION ===============================================================================================

    # Get probability vector for next character, given a string (sequence)
    # def get_pvec(self, sequence: str, context=0):
    #     # By default, context is set to the number of grams
    #     context = max(context, 0)
    #     if context == 0:
    #         context = self.grams-1
    #     context = min(context, self.grams-1)
    #     key = sequence[-context:]
    #     # Pull probability vector from P
    #     if key in self.P:
    #         p = self.P[key]
    #     else:
    #         p = np.ones(len(self.charset), dtype=np.float16)
    #         p /= sum(p)
    #     return p

    # Converts a probability vector p to a readable string
    # Meant for debug or visualizations
    def pvec_to_str(self, pvec: np.array):
        string = ''
        for i in range(len(self.charset)):
            if pvec[i] != 0.0:
                string += f'{self.charset[i]}: {pvec[i] * 100:0.2f}%\n'
        return string

    def get_branch(self, sequence, context):
        key = sequence[-context:]
        if key in self.B:
            branch = self.B[key]
        else:
            branch = self.charset
        return branch

    # Doesn't work properly
    # def prune_b(self, exclusions: [str]):
    #     for exclusion in exclusions:
    #         key = exclusion[:-1]
    #         print(f'key: {key}')
    #         print(f'index: {exclusion[-1]}')
    #         if key in self.B:
    #             self.B[key] = self.B[key].replace(exclusion[-1], '')

    # GENERATION ======================================================================================================

    # Recursively traverses dataset
    def _recursive_list(self, target_length, context, sequence=None):
        wordlist = []  # Wordlist starts empty for each recursion
        if sequence is None:  # If the sequence is empty, start a new sequence
            sequence = self.charset[0]
        curr_length = len(sequence)
        if curr_length == 2:
            print(f'ngram: Generating {target_length}-gram \'{sequence[1]}\' sequences...')
        branch = self.get_branch(sequence, context)  # Get next branch
        if curr_length == target_length+1:  # If the sequence must end now...
            if branch[0] == self.charset[0]:   # And the sequence CAN end now, complete the sequence.
                wordlist.append(sequence[1:])
            return wordlist
        if branch[0] == self.charset[0]:  # Don't end the sequence too early.
            branch = branch[1:]
        for char in branch:
            wordlist += self._recursive_list(target_length, context, sequence + char)
        return wordlist

    # Calls _recursive_list for each length between min_length and max_length
    def exhaustive_list(self, min_length, max_length, gamma=DEFAULT_GAMMA):
        wordlist = []
        for length in range(min_length, max_length+1):  # For each possible length of word...
            context = self.dynamic_context(length, gamma)  # Dynamically set context window length...
            print(f'ngram: Generating {length}-gram sequences with context length {context}...')
            wordlist += self._recursive_list(length, context)  # And pass both values to _recursive_list.
        print(f'ngram: Done generating.')
        return wordlist

    # Choose a random character, weighted by probability vector p
    # def sample(self, pvec: [float]):
    #     return random.choices(self.charset, weights=pvec)[0]

    # Probabilistically extrapolate next character in sequence
    # def extrap_next(self, sequence: str, context=0, beta=-1.0):
    #     pvec = self.get_pvec(sequence, context)
    #     if beta != -1.0:
    #         pvec = self.sinoid(pvec, beta)
    #     char = self.sample(pvec)
    #     return char

    # Extrapolate next character in sequence, choose only most probable character
    # def extrap_next_best(self, sequence: str, context=0):
    #     pvec = self.get_pvec(sequence, context)
    #     index = np.argmax(pvec)
    #     return self.charset[index]

    # Generate a sequence (word) from scratch, based on N dataset
    # def gen_sequence(self, min_length=0, max_length=100, context=0, beta=-1.0, gamma=DEFAULT_GAMMA):
    #     # By default, context is dynamic.
    #     if context == 0:
    #         context = self.dynamic_context(max_length, gamma)
    #     # Iteratively extrapolate next characters until <END> character is drawn
    #     sequence = self.charset[0]
    #     while True:
    #         curr_char = self.extrap_next(sequence, context, beta)
    #         sequence += curr_char
    #         if curr_char == self.charset[0]:
    #             break
    #         if len(sequence) > max_length+2:
    #             break
    #     # If sequence does not meet length requirements, try again
    #     if len(sequence) > max_length+2 or len(sequence) < min_length+2:
    #         return self.gen_sequence(min_length, max_length, context, beta)
    #     # Truncate <START> and <END> characters
    #     sequence = sequence[1:-1]
    #     return sequence