import csv
import jellyfish._jellyfish as py_jellyfish

### HEADER UTILITIES

# Params: filepath = path to given CSV file as a String
#         input_str = given String to which we compare
# Return: [(other_header, value), ... ]
def cmp_str_to_hdr(input_str, filepath):
    headers = get_headers(filepath)
    total_dists = []
    for header in headers:
        lev_dist = calc_lev_dist(input_str, header)
        ham_dist = calc_ham_dist(input_str, header)
        jar_dist = calc_jar_dist(input_str, header) * 5
        total_cur = "%.3f" % (lev_dist + ham_dist - jar_dist)
        total_cur = max(0, float(total_cur))
        total_dists.append((header, total_cur))
        total_dists.sort(key = lambda x: x[1])
    return total_dists


# Params: filepath = path to given CSV file as a String
# Return: [ ( header, [ (other_header, value) ... ] ) ... ]
def cmp_hdrs(filepath):
    headers = get_headers(filepath)
    total_dists = []
    for header in headers:
        other_headers = list(headers)
        other_headers.remove(header)
        total_dist_cur = []
        for other_header in other_headers:
            lev_dist = calc_lev_dist(header, other_header)
            ham_dist = calc_ham_dist(header, other_header)
            jar_dist = calc_jar_dist(header, other_header) * 5
            total_cur = "%.3f" % (lev_dist + ham_dist - jar_dist)
            total_cur = max(0, float(total_cur))
            total_dist_cur.append((other_header, total_cur))
            total_dist_cur.sort(key = lambda x: x[1])
        total_dists.append((header, total_dist_cur))
    return total_dists


# Params: key = given String to test for
#         filepath = path to given CSV file as a String
# Return: [header, header, ... ] or [] if N/A
def get_hdrs_to_str(key, filepath):
    headers = get_headers(filepath)
    contained = []
    for header in headers:
        if key in header:
            contained.append(header)
        elif header in key:
            contained.append(header)
    return contained


### CSV Util Functions

# Params: file = path to given CSV file as a String
# Return: [ header1, header2, ... ]
def get_headers(file):
    headers = []
    with open(file) as f:
        reader = csv.reader(f)
        headers = next(reader)
    return headers


### LEVENSHTEIN DIST

# Params: a = String, b = String
# Return: Levenshtein Distance
def calc_lev_dist(a, b):
    return py_jellyfish.damerau_levenshtein_distance(a, b)


### JARO-WINKLER DIST

# Params: a = String, b = String
# Return: Jaro-Winkler Distance
def calc_jar_dist(a, b):
    return py_jellyfish.jaro_winkler(a, b)


### HAMMING DIST

# Params: a = String, b = String
# Return: Hamming Distance
def calc_ham_dist(a, b):
    return py_jellyfish.hamming_distance(a, b)
