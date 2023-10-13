'''
Semantic Similarity

Authors: Michael Guerzhoy (starter code, last modified: Nov. 18, 2022) and Tanvi Manku (completed functions, last modified Dec. 9, 2022)

Notes: Use any .txt file of coherent and sensible sentences, such as a book, for semantic similarity computation.

       Use synonym_questions.txt to test the accuracy of the system for synonym selecting- each line in synonym_questions.txt represents
       a question, where the first word is the word to find a synonym for, and the remaining words are possible answers for the system
       to select from.
'''

import math

def norm(vec):
    '''
    Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''
    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    """
    Purpose:
    - Calculate the cosine similarity of two vectors

    Parameters:
    - vec1 -- the first sparse vector's semantic descriptor, as a dictionary
    - vec2 -- the second sparse vector's semantic descriptor, as a dictionary

    Returns:
    - Float representing the cosine similarity

    Assumes:
    - vec1 and vec2 are not empty dictionaries
    """

    dot = 0

    # Magnitude of vec1
    mag_1 = 0

    # Magnitude of vec2
    mag_2 = 0

    for i in vec1:

        # Calculating the "dot product"
        if i in vec2:
            dot += vec1[i] * vec2[i]

        mag_1 += vec1[i] ** 2

    for j in vec2:
        mag_2 += vec2[j] ** 2

    mag_1 = math.sqrt(mag_1)
    mag_2 = math.sqrt(mag_2)

    mag_prod = mag_1 * mag_2

    sim = dot / mag_prod

    return sim


def build_semantic_descriptors(sentences):
    """
    Purpose:
    - Create the semantic descriptor

    Parameters:
    - sentences -- a list of sentences, containing sub-lists of words

    Returns:
    - Dictionary representing the semantic descriptor

    Assumes:
    - Words repeated in a sentence are only counted once
    """
    d = {}

    for s in sentences:
        all = []
        for w in range(0, len(s)):
            word = s[w].lower()

            others = []

            if word not in d and word not in all:
                d[word] = {}

            if word not in all:
                for i in range(0, len(s)):
                    other = s[i].lower()
                    if other != word and other not in others:
                        others.append(other)

                for j in others:
                    if j not in d[word]:
                        d[word][j] = 1
                    else:
                        d[word][j] += 1

                all.append(word)

    return d

def build_semantic_descriptors_from_files(filenames):
    """
    Purpose:
    - Create the semantic descriptor from files

    Parameters:
    - filenames -- a list of file names to build the semantic descriptor from

    Returns:
    - Dictionary representing the semantic descriptor

    Assumes:
    - ".", "!", "?" are the only punctation seperating sentences
    - ",", "--", "-", ":", ";", " ", "'", "”", "“", ")", "(", '"', " ", "''" are the only other punctuation present in the text
    - A newline on its own does not represent a new sentence
    """
    sent = []

    for n in range(0, len(filenames)):

        file = open(filenames[n], "r", encoding="utf-8")

        text = file.read().strip().lower()

        text = text.replace("\n", " ")

        for sen_char in [".", "!", "?"]:
            text = text.replace(sen_char, "/n")

        text = text.split("/n")

        for l in text:
            if l == "":
                text.remove(l)

        for line in text:
            line = line.strip(" ")
            line = line.strip('"')
            line = line.strip("\n")
            line = line.strip()

            for word_char in [",", "--", "-", ":", ";", " ", "'", "”", "“", ")", "(", '"', " ", "''"]:
                line = line.replace(word_char, "\n")

            line = line.split("\n")

            temp = []

            for w in line:
                if w != "" and w != " ":
                    temp.append(w)

            line = temp

            sent.append(line)

    dic = build_semantic_descriptors(sent)

    return dic


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    """
    Purpose:
    - Determine the most similary word/best synonym for a word

    Parameters:
    - word -- the word to find a synonym for
    - choices -- the words to choose a synonym from
    - semantic_descriptors -- a semantic descriptor
    - similarity_fn -- the similarity function to compute the similarity between two words

    Returns:
    - A string- the word from choices that is most similar to the word

    Assumes:
    - semantic_descriptors is a dictionary
    - the first word in choices should be returned if there is a tie or if the similarity cannot be computed for all choices with the word
    """
    res = {}

    if word not in semantic_descriptors:
        return choices[0]
    else:
        word_desc = semantic_descriptors[word]

        for choice in choices:

            commons = 0

            if choice not in semantic_descriptors:
                res[choice] = -1
            else:
                choice_desc = semantic_descriptors[choice]
                for w in word_desc.keys():
                    if w in choice_desc.keys():
                        commons += 1

                if commons == 0:
                    res[choice] = -1
                else:
                    res[choice] = similarity_fn(word_desc, choice_desc)

        max_i = 0

        for c in range(1, len(choices)):

            if res[choices[c]] > res[choices[c - 1]]:
                max_i = c

        max_word = choices[max_i]

    return max_word


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    """
    Purpose:
    - Determine the percentage of questions answered correctly using most_similar_word()

    Parameters:
    - filename -- the name of the file containing the questions to be tested
    - semantic_descriptors -- a semantic descriptor
    - similarity_fn -- the similarity function to compute the similarity between two words

    Returns:
    - A float from 0 to 100 representing the percentage of questions answered correctly

    Assumes:
    - the questions in filename are in the same format as test.txt in the handout
    - semantic_descriptors is a dictionary
    """

    test_file = open(filename, "r", encoding="latin1")
    qs = test_file.read()

    qs = qs.split("\n")

    total = len(qs)

    correct = 0

    for q in qs:
        q = q.split(" ")

        test_word = q[0]
        cor_ans = q[1]
        options = q[2:]

        most_similar = most_similar_word(test_word, options, semantic_descriptors, similarity_fn)

        if most_similar == cor_ans:
            correct += 1

    percent = correct/total * 100

    return percent
