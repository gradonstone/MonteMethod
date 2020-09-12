import monte_method as mm
import matplotlib.pyplot as plt

INPUT_FILE = "bigram_log_format1.txt"

def Sort_Tuple(tup):
    tup.sort(key = lambda x: x[1], reverse = True)
    return tup

if __name__ == "__main__":

    fig, ax = plt.subplots()


    bigram_matrix = mm.get_bigram_matrix(INPUT_FILE)
    bigram_list = []
    total = 0.0
    for key, value in bigram_matrix.items():
        bigram_list.append((key,value))

    bigram_list = Sort_Tuple(bigram_list)
    labels = []
    values = []
    for x in bigram_list[:15]:
        labels.append(x[0])
        values.append(x[1])

    ax.barh(labels, values)
    ax.invert_yaxis()

    
    plt.show()