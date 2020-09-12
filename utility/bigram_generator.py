import math


WAR_FILE    = "war-and-peace.txt"
BIGRAM_FILE = "bigram.txt"


f1 = open(WAR_FILE)

bigrams = {} # string:value pair, where string is bigram (ie 'th')
             # and value is the number of times it appeared

x = 0

# gives total of each bigram

total_bigrams = 0

while True:
    c1 = f1.read(1)
    c2 = f1.read(1)
    f1.seek(f1.tell() - 1, 0)
    x = x + 1
    if not c1:
        break
    if not c2:
        break
    if (ord(c1) < ord('a')) or (ord(c1) > ord('z')):
        continue
    if (ord(c2) < ord('a')) or (ord(c2) > ord('z')):
        continue

    cur_bigram = c1 + c2
    if cur_bigram in bigrams:
        bigrams[cur_bigram] += 1
    else:
        bigrams[cur_bigram] = 1


total_bigrams = 0
for bg, total in bigrams.items():
    total_bigrams += total

# add all unfound possibilities
ch1 = 'a'
# need SOME possibility 
while ord(ch1) <= ord('z'):
    ch2 = 'a'
    while (ord(ch2) <= ord('z')):
        bigram = ch1 + ch2
        if bigram not in bigrams:
            bigrams[bigram] = 1.0 / total_bigrams
        ch2 = chr(ord(ch2) + 1)
    ch1 = chr(ord(ch1) + 1)

print(len(bigrams))


f2 = open(BIGRAM_FILE, "w")
for bg, total in bigrams.items():
    bigram_frequency = math.log(float(total)/total_bigrams, 10)
    f2.write("{}: {}\n".format(bg, bigram_frequency))





