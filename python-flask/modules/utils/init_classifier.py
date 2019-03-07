from modules.DataTraining import driver as classfier
from jsonmerge import merge
import json


def classify_data(category, headers, filepaths):
    headers_unwrap = headers.get_json().split(',')
    category_unwrap = category.get_json()
    ontology = merge(category, headers)
    print(ontology)
    classfier.classify(ontology, filepaths)

