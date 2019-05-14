import csv
from modules.DataTraining import spacys_mom as spm
import wordninja as wj
import numpy as np

### SPACY STUFF

nlp = spm.SpacyWrapper()

def find_similar(properties, filepath):
    # Load spaCy's NLP dictionaries
    # Slice and Lemmatize properties
    properties_sl = []
    for prop in properties:
        prop_sl = split_and_lemmatize(prop)
        properties_sl.append(prop_sl)
    # Get ALL column headers from file
    headers = get_headers(filepath)
    # Slice and Lemmatize all headers
    headers_sl = []
    for header in headers:
        header_sl = split_and_lemmatize(header)
        headers_sl.append(header_sl)
    # Compare each property to each header
    classification = {}
    for index in range(len(properties)):
        classification[properties[index]] = cmp_prop_to_headers(properties[index], headers, properties_sl[index], headers_sl)
    # Populate dict and return
    results = (filepath, classification)
    return results

### Comparison Functions

# NOTE: Both prop_sl and headers_sl may be broken
#       into multiple English words, so they are
#       ARRAYS not STRINGS
def cmp_prop_to_headers(orig_prop, orig_headers, prop_sl, headers_sl):
    # Loop over each property's words
    related_headers = []
    for index in range(len(orig_headers)):
        header_sl = headers_sl[index]
        is_related = cmp_prop_to_header(prop_sl, header_sl)
        if is_related:
            related_headers.append(orig_headers[index])
    return related_headers   

def cmp_prop_to_header(prop_sl, header_sl):
    means_all = []
    for word in prop_sl:
        word_spacy = nlp.process(word)
        cmp_values = []
        for header in header_sl:
            header_spacy = nlp.process(header)
            sim_value = nlp.compare(word_spacy, header_spacy)
            # If a lemmatized word from both header and property
            # are very closely related, return it regardless
            # of overall average. 
            if sim_value > 0.95:
                return True
            else:
                cmp_values.append(sim_value)
        mean_hdr = np.mean(cmp_values)
        means_all.append(mean_hdr)
    mean_all = np.mean(means_all)
    # TODO: Strictness of "relatedness" needs tweaking. 
    if mean_all > 0.8:
        return True
    else:
        return False

### Util Functions

def split_and_lemmatize(input):
    split_words = slice_word(input)
    input_lemma = []
    for word in split_words:
        word_tok = nlp.process(word)
        word_lemma = lemmatize_word(word_tok)
        input_lemma.append(word_lemma)
    return input_lemma

# Params: input = a spaCy token
# Return: String
# EX: "reviews" -> "review"
# EX: "thought" -> "think"
def lemmatize_word(input):
    return input[0].lemma_

# Params: input = given String
# Return: [sub-word1, sub-word2, ...]
# EX: "review_date" -> ['review', 'date']
# EX: "reviewernameslast" -> ['reviewer', 'names', 'last']
def slice_word(input):
    return wj.split(input)

# Params: file = path to given CSV file as a String
# Return: [ header1, header2, ... ]
def get_headers(file):
    headers = []
    with open(file) as f:
        reader = csv.reader(f)
        headers = next(reader)
    return headers
