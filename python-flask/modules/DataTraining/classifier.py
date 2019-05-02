from modules.DataTraining import headers as hdr
from flask import jsonify
import json

class Classifier:
    # Params: data_filepaths = paths to 1+ CSV files
    def __init__(self, data_filepaths):
        self.data_filepaths = data_filepaths

    # Params: ontology = JSON object passing 
    # Returns: classification metadata
    def classify_ontology(self, ontology):
        # Once I deconstruct the JSON object (the ontology) I get passed, 
        # I will use that for comparison. For now just compare based on
        # similarity between headers.
        headers_results = []
        category = ontology[0]
        properties = ontology[1]
        for filepath in self.data_filepaths:
            headers_results.append(hdr.find_similar(properties, filepath))
        # Translate to agreed contract w/ backend
        results = {}
        for prop in properties:
            results[prop] = {}
            for f, dict_res in headers_results:
                if f not in results[prop].keys():
                    results[prop][f] = dict_res[prop]
                else:
                    results[prop][f].append(dict_res[prop])
        finalized = {category: results}
        return finalized
