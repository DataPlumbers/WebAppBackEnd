# Driver for ML component of MarkLogic Classifier.
import sys
from modules.DataTraining import classifier as cfr
# import classifier as cfr
import os.path

# Params: ontology = stuff passed by frontend
#         filepaths = list of filepaths to CSV files
# Returns: The classification metadata
# TODO: More clearly specify what metadata to return
def classify(ontology, filepaths):
    # Verify parameters
    if len(filepaths) == 0 or len(ontology) != 2:
        print_usage()
        raise ValueError("Bad arguments for Driver.classify")
    for filepath in filepaths:
        if not os.path.isfile(filepath):
           raise FileNotFoundError(str(filepath) + " couldn't be found.")
    my_classifier = cfr.Classifier(filepaths)
    results_json = my_classifier.classify_ontology(ontology)
    print(results_json)
    return results_json


# Print correct usage of application.
def print_usage():
    print("""Classification module requires two parameters:
             1) The given ontology as a JSON object.
                Ex: ("myCategory", ["val1", "val2"])
             2) One or more CSV filepaths.
                Ex: ["file1.csv", "file2.csv"]""")
