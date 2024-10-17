"""
wordlist_utils v0.1 WIP
"""

alphabet = 'abcdefghijklmnopqrstuvwxyz'
cons = 'bcdfghjklmnpqrstvwxz'
vows = 'aeiouy'


# Build default illegal lists ==============================

def char_zip(char1: str, chars2: str):
    char1 = char1 * len(chars2)
    zipped = [item[0] + item[1] for item in zip(char1,  chars2)]
    return zipped


illegal_words = []
illegal_starts = []
illegal = []

# Three of the same letter is illegal
for letter in alphabet:
    illegal.append(letter * 3)


# List Operations ======================================================================================================

def remove_duplicates(_list: []):
    _list = list(dict.fromkeys(_list))
    return _list


def remove_illegal_strs(_list: [str]):
    _list = [i for i in _list if str_is_legal(i)]
    return _list


# Returns list of items that are in list a but NOT in list b
def in_a_not_in_b(a: [], b: []):
    c = [i for i in a if i not in b]
    c.sort()
    return c


# String Operations ====================================================================================================


# Boolean; is the string comprised entirely of consonants
def str_is_all_cons(string: str):
    if not string.islower():
        string = string.lower()
    for vow in vows:
        if vow in string:
            return False
    return True


# Boolean; does the string pass checks against illegal lists
def str_is_legal(string: str):
    if not string.islower():
        string = string.lower()
    for i in illegal:
        if i in string:
            print(f"wordlist_utils: {string} is illegal.")
            return False
    for i in illegal_starts:
        if string.startswith(i):
            print(f"wordlist_utils: {string} is illegal.")
            return False
    for i in illegal_words:
        if string == i:
            print(f"wordlist_utils: {string} is illegal.")
            return False
    if str_is_all_cons(string):
        print(f"wordlist_utils: {string} is illegal.")
        return False
    return True


# Puts spaces ahead of all uppercase letters to split up 'camel case' and acronyms
def str_split_camelcase(string: str):
    for i in reversed(range(len(string))):
        if string[i].isupper():
            string = string[:i] + ' ' + string[i:]
    return string


# Replaces punctuation marks with spaces
def str_remove_punc(string: str):
    punctuation = '`-=[];\',./~!@#$%^&*()_+{}|:"<>?'
    for char in punctuation:
        string = string.replace(char, ' ')
    return string


# Parses string into distinct words
def str_extract_wordlist(string: str):
    string = str_split_camelcase(string)
    string = str_remove_punc(string)
    words = string.split()
    words = [word.lower() for word in words
             if word.isalpha()
             and word.isascii()
             and len(word) > 2
             and str_is_legal(word.lower())]
    words = remove_duplicates(words)
    words.sort()
    return words


# File Operations ======================================================================================================

# Reads in a wordlist directly from a wordlist file
def fr_import_wordlist(filename: str):
    print(f'wordlist_utils: Importing wordlist from {filename} ...')

    with open(filename, 'r') as f:
        wordlist = f.readlines()
    wordlist = [word[:-1] for word in wordlist]  # Remove \n chars

    print(f'wordlist_utils: Finished importing words.')
    return wordlist


# Extracts words from a file, outputs a wordlist
def fr_extract_words(filename: str):
    print(f'wordlist_utils: Extracting words from {filename} ...')

    with open(filename, 'r') as f:
        lines = f.readlines()
    wordlist = []
    for line in lines:
        wordlist += str_extract_wordlist(line)
    wordlist = remove_duplicates(wordlist)
    wordlist.sort()

    print(f'wordlist_utils: Finished extracting words.')
    return wordlist


# Extracts only unique words from a file, given a wordlist file of known words (mask_filename)
def fr_extract_words_filtered(filename: str, mask_filename: str):
    print(f'wordlist_utils: Extracting unique words from {filename} with mask {mask_filename} ...')

    wordlist = fr_extract_words(filename)
    mask = fr_import_wordlist(mask_filename)
    print('wordlist_utils: Filtering (this may take a while) ...')
    filtered_wordlist = []
    n = 20
    for i in range(n):
        split0 = int((len(wordlist) / n) * i)
        split1 = int((len(wordlist) / n) * (i + 1))
        filtered_wordlist += in_a_not_in_b(wordlist[split0:split1], mask)
        print(f'{i/n * 100:0.2f}% ...')

    filtered_wordlist.sort()
    print(f'wordlist_utils: Finished extracting unique words.')
    return filtered_wordlist


# Extracts only unique words from a file, then writes those words to a new file.
def frw_extract_filter_export(filename: str, source_filename: str, mask_filename: str):
    words = fr_extract_words_filtered(source_filename, mask_filename)
    fw_export_wordlist(filename, words)


# Saves a wordlist to a new wordlist file (overwrites)
def fw_export_wordlist(filename: str, wordlist: [str]):
    print(f'wordlist_utils: Exporting wordlist to {filename} ...')
    wordlist.sort()
    with open(filename, 'w') as f:
        for word in wordlist:
            f.write(word)
            f.write('\n')
    print(f'wordlist_utils: Finished exporting wordlist.')


# Adds a wordlist to an existing wordlist file, removes duplicates
def fa_add_to_wordlist(filename: str, wordlist: [str]):
    print(f'wordlist_utils: Adding to existing wordlist file: {filename} ...')

    wordlist += fr_import_wordlist(filename)
    wordlist = remove_duplicates(wordlist)
    wordlist.sort()
    fw_export_wordlist(filename, wordlist)

    print(f'wordlist_utils: Finished adding to file.')
