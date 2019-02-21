# Driver for ML component of MarkLogic Classifier.
import sys
from modules.DataTraining import classifier as cfr


# Params: ontology = JSON object passed by frontend
#         arg = list of CSV file paths
# Returns: The classification metadata
# TODO: More clearly specify what metadata to return
def classify(ontology, *arg):
    # Verify parameters
    if len(arg) == 0:
        print_usage()
    my_classifier = cfr.Classifier(arg)
    results = my_classifier.classify_ontology(ontology)
    return results


# Print correct usage of application.
def print_usage():
    print("""driver.py requires two parameters:
             1) The given ontology as a JSON object.
             2) One or more CSV filepaths.""")
    sys.exit(2)

