import string
import math

def read_collocations(file_path):
    with open(file_path, 'r') as f:
        return [line.strip().replace("\n", "") for line in f.readlines()]

def tokenize_collocations(collocations):
    return [line.split(' ') for line in collocations]

def filter_punctuation(collocations):
    return [[token for token in line if token not in string.punctuation] for line in collocations]

def count_unigrams(collocations):
    unigram_freq = {}
    total_unigrams = 0
    for line in collocations:
        for token in line:
            total_unigrams += 1
            if token not in unigram_freq:
                unigram_freq[token] = 1
            else:
                unigram_freq[token] += 1
    return unigram_freq, total_unigrams

def create_bigrams(collocations):
    bigrams = []
    total_bigrams = 0
    for line in collocations:
        for i in range(len(line) - 1):
            total_bigrams += 1
            bigrams.append(line[i] + ' ' + line[i + 1])
    return bigrams, total_bigrams

def count_bigrams(bigrams):
    bigram_freq = {}
    for bigram in bigrams:
        if bigram not in bigram_freq:
            bigram_freq[bigram] = 1
        else:
            bigram_freq[bigram] += 1
    return bigram_freq

def calculate_chi_squared(bigram, unigram_freq, bigram_freq, total_unigrams):
    w1, w2 = bigram.split(' ')
    O = bigram_freq[bigram]
    E = (unigram_freq[w1] * unigram_freq[w2]) / total_unigrams
    return total_unigrams * (O - E)**2 / (unigram_freq[w1] * unigram_freq[w2])

def calculate_pmi(bigram, unigram_freq, bigram_freq, total_unigrams, total_bigrams):
    w1, w2 = bigram.split(' ')
    p_bigram = bigram_freq[bigram] / total_bigrams
    p_w1 = unigram_freq[w1] / total_unigrams
    p_w2 = unigram_freq[w2] / total_unigrams
    return math.log2(p_bigram / (p_w1 * p_w2))

if __name__ == "__main__":
    collocations = read_collocations('Collocations')
    collocations = tokenize_collocations(collocations)
    collocations = filter_punctuation(collocations)
    
    unigram_freq, total_unigrams = count_unigrams(collocations)
    bigrams, total_bigrams = create_bigrams(collocations)
    bigram_freq = count_bigrams(bigrams)
    
    chi_squared = {bigram: calculate_chi_squared(bigram, unigram_freq, bigram_freq, total_unigrams) for bigram in bigram_freq}
    pmi = {bigram: calculate_pmi(bigram, unigram_freq, bigram_freq, total_unigrams, total_bigrams) for bigram in bigram_freq}
    
    ranked_bigrams = sorted(chi_squared, key=chi_squared.get, reverse=True)
    
    print('Top 20 bigrams by chi-squared value:')
    for i in range(20):
        print(f"{i+1}. {ranked_bigrams[i]}")
