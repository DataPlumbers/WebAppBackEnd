# Reference: https://spacy.io/usage/linguistic-features

import spacys_mom as spm
import pandas as pd
from dateparser.search import search_dates

nlp = spm.SpacyWrapper()


def get_entities_file(filepath):
    # Get CSV file as a Data Frame (df)
    df = pd.read_csv(filepath, delimiter=',', encoding='utf-8-sig')
    #print(df)
    # Iterate over each column in Data Frame
    ent_dict = {}
    for column in df:
        ent = get_entities_col(df[column])
        ent_dict[column] = ent
    return ent_dict


def get_entities_col(column):
    # Loop over each value in the column
    col_ents = []
    for value in column:
        valstr = str(value)
        # Evaluate each value in spaCy
        # NOTE: a "value" can be anything (number, sentence, etc.)
        doc = nlp.process(valstr)
        val_ents = [e.label_ for e in doc.ents]
        if len(val_ents) != 0:
            # Get most common entity type
            most_common_ent = max(set(val_ents), key=val_ents.count)
            col_ents.append(most_common_ent)
        # TODO: Override Cardinal pretty often...
        try:
            float(valstr)
        except ValueError:
            if search_dates(valstr) != None:
                col_ents.append("DATE")
    df = pd.DataFrame(col_ents)
    # Hacky fix for cases when there isn't an entity associated with a header
    # We can do something more elegant here...
    try:
        res = df.mode()[0][0]
        return res
    except KeyError:
        pass
