from modules.DataTraining import app as classfier
from jsonmerge import merge


def classify_data(category, headers, filepaths):
    ontology = merge(category, headers)
    classfier.classify(ontology, filepaths)
