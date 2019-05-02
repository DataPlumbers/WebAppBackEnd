from modules.DataTraining import driver as driver
from jsonmerge import merge
import json


def classify_data(category, headers, filepaths):
    headers_unwrap = headers.split(',')
    category_unwrap = category
    ontology = merge(category_unwrap, headers_unwrap)
    print(ontology)
    return driver.classify(ontology, filepaths)

