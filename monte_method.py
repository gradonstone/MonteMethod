import random
import math
import sys

INPUT_FILE   = "testInput.txt"
BIGRAM_FILE  = "bigram.txt"
OUTPUT_FILE  = "output.txt"

FIRST_GUESS  = "abcdefghijklmnopqrstuvwxyz" # first guess for algo
CHAIN_STEPS  = 10000                         # how many steps before terminate    


# key_mapping -> {'a': 't', ... , 'z':'b'}
# bigram_matrix -> {'th': -8.67, ... }
# Bigram matrix is dictionary of string:values from War and Peace novel. 
# Transition_function is the arbitrary "key" we determined 
# Returns the log(plausibility_product)
# Remember log(a*b) = log(a) + log(b)
# therefore, log(a*b* ... *z) = log(a) + log(b) + ... + log(z)
def plausibility_log(bigram_matrix, ciphertext, key_mapping):
    plausibility_product = 0
    for x in range(0, len(ciphertext) - 1):
        s1     = ciphertext[x]
        s2     = ciphertext[x + 1]
        f_s1   = key_mapping[s1] # return character
        f_s2   = key_mapping[s2] # return character
        bigram = f_s1 + f_s2
        if (bigram in bigram_matrix):
            plausibility_product += bigram_matrix[bigram]
        else:
            print("Error! Bigram '{}'' not found in matrix".format(bigram))
    return plausibility_product


def is_lower_char(ch):
    if (ord(ch) < ord('a') or ord(ch) > ord('z')):
        return False
    return True

# Returns a key:value matrix of letter:frequency
# from file_name, a bigram file formatted:
# af: -8.675432
# bg: -5.1341234
# .
# .
# .
def get_bigram_matrix(file_name):
    bigram_matrix = {}
    f             = open(file_name)
    line          = f.readline()
    while line:
        line   = line.strip()
        bigram = line[:2]
        freq   = float(line[4:])
        bigram_matrix[bigram] = freq
        line   = f.readline()
    return bigram_matrix

# Returns array of all letters, ordered, from file_name
def read_letters_from_file(file_name):
    letters_from_file = []
    f1                = open(file_name, "r")
    while True:
        c1 = f1.read(1)
        if not c1:
            break
        if (ord(c1) < 0x61) or (ord(c1) > 0x7a):
            continue
        letters_from_file.append(c1)
    return letters_from_file

# If you want a a custom key:mapping input from user
def get_key_mapping():
    key_mapping = {}
    input_str   = input("Type map: ")
    cur_letter  = 'a'
    for x in input_str:
        key_mapping[x] = cur_letter
        cur_letter     = chr(ord(cur_letter) + 1)
    return key_mapping

# Returns map of letter:letter of type:
# {'a':str[0], 'b':str[1], ..., z:str[25]}
# TO DO: Error checking on str
def assign_key_mapping(str):
    key_mapping = {}
    cur_letter  = 'a'
    for x in str:
        key_mapping[x] = cur_letter
        cur_letter     = chr(ord(cur_letter) + 1)
    return key_mapping

# Transposes the key_mapping to a random new key
# mapping with 2 values switched betweem the keys.
# Returns a new transposed map of letter:letter
def transpose_key_mapping(key_mapping):
    transposed_map = key_mapping.copy()
    rand1          = random.randint(0,25)
    rand2          = random.randint(0,25)
    # make sure values are unique
    while (rand1 == rand2):
        rand2 = random.randint(0,25)

    letter_ord_1 = ord('a') + rand1
    letter_ord_2 = ord('a') + rand2
    temp_char    = transposed_map[chr(letter_ord_1)]
    transposed_map[chr(letter_ord_1)] = transposed_map[chr(letter_ord_2)]
    transposed_map[chr(letter_ord_2)] = temp_char
    return transposed_map

# Flips a log based probability coin.
# True = Heads
def flip_probability_coin(new_p, old_p):
    prob = new_p - old_p
    prob = 10 ** prob
    if (random.random() < prob):
        return True
    else:
        return False

# Prints the contents of input_file after letter_mapping
# transition applied to the screen
def print_transposition(input_file, letter_mapping):
    f  = open(input_file, "r")
    ch = f.read(1)
    while ch:
        if (is_lower_char(ch)):
            ch = letter_mapping[ch]
        print(ch, end="")
        ch = f.read(1)

def get_encryption_key_as_string(key_mapping):
    # switch keys and values
    key_string           = ""
    key_mapping_switched = {}
    for key, value in key_mapping.items():
        key_mapping_switched[value] = key
    ch = 'a'
    while (ord(ch) <= ord('z')):
        key_string += key_mapping_switched[ch]
        ch         = chr(ord(ch) + 1)
    return key_string

def transpose_ciphertext_and_write_results_to_file(ciphertext_file, 
    key_mapping, output_file):
    in_f  = open(ciphertext_file, "r")
    out_f = open(output_file, "w")

    # write encryption key
    out_f.write("Encryption key: {}\n\nPlaintext:\n\n"
        .format(get_encryption_key_as_string(key_mapping)))
    ch = in_f.read(1)
    while ch:
        if (is_lower_char(ch)):
            ch = key_mapping[ch]
        out_f.write(ch)
        ch = in_f.read(1)

def monte_method(prelim_guess, bigram_file, ciphertext_file):
    # start with preliminary guess and assign to key_mappings
    key_mapping   = assign_key_mapping(prelim_guess)
    bigram_matrix = get_bigram_matrix(bigram_file)
    file_letters  = read_letters_from_file(ciphertext_file)

    # calculate plausibility
    plausibility  = plausibility_log(bigram_matrix, file_letters, key_mapping)
    
    # print_transposition(INPUT_FILE, key_mapping)
    # change to new key mapping 
    for i in range(0, CHAIN_STEPS):
        new_mapping      = transpose_key_mapping(key_mapping)
        new_plausibility = plausibility_log(bigram_matrix, file_letters, new_mapping)
        if (new_plausibility > plausibility):
            key_mapping  = new_mapping
            plausibility = new_plausibility
        else:
            # flip (new_plausibility / plausbility) coin, 
            # if heads
                # accept new_mapping
            # else
                # keep key_mapping
            if(flip_probability_coin(new_plausibility, plausibility)):
                key_mapping  = new_mapping
                plausibility = new_plausibility

    return key_mapping

if __name__ == "__main__":

    if (len(sys.argv) != 2 and len(sys.argv) != 3):
        sys.exit("usage: {} <ciphertext_file> <optional_output_file>".format(sys.argv[0]))
    if (len(sys.argv) == 3):
        output_file = sys.argv[2]
    else:
        output_file = OUTPUT_FILE

    ciphertext_file = sys.argv[1]
    key_mapping     = monte_method(FIRST_GUESS, BIGRAM_FILE, ciphertext_file)
    transpose_ciphertext_and_write_results_to_file(ciphertext_file, key_mapping, output_file)
    print("Results outputed to {}".format(output_file))
