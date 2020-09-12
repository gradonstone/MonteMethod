###############################################################################
#                                                                             #
# summary:                                                                    #
#     monte_method.py requires one command line arguments, <ciphertext_file>, #
#     and an optional argument, <optional_output_file>. Both are file names,  #
#     where <ciphertext_file> points to an input file to be run through the   #
#     Monte Method and <optional_output_file> is formatted with the           #
#     encryption key and plaintext after decrypting                           # 
#                                                                             #
#  authors: Samantha Chaves, Sam Ostlund, Gradon Stone                        #
#                                                                             #
###############################################################################

###############################################################################
#                                                                             #
# usage:                                                                      #
#    python3 monte_method.py <ciphertext_file> <optional_output_file>         #
#                                                                             #
# important constants inside monte_method:                                    #
#                                                                             #
#    - CHAIN_STEPS: number of steps run before halting the algorithm          #
#                                                                             #
#    - OUTPUT_FILE: default file for outputting results                       #
#                                                                             #
###############################################################################

###############################################################################
#                                                                             #
# requirements:                                                               #
#    python3                                                                  #
#                                                                             #
###############################################################################