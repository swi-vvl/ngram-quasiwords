import quasiword as qw
import cProfile


def reset_and_learn():
    qw.reset()
    qw.learn_wordlist_file('english_wordlist.txt')
    qw.autolearn()


def load_and_generate():
    # qw.init()
    qw.generate_wordlist(3, 8)


# This function will convert english_wordlist.txt into a list of 345,000,000 quasiwords.
def generate_345m_list():
    qw.reset()
    qw.learn_wordlist_file('english_wordlist.txt')
    qw.autolearn(gamma=0.62)
    qw.generate_wordlist(3, 8)


# Main code here
generate_345m_list()
