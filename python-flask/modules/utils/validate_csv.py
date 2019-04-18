import csv

def validate_csv_file(filename):
    csv_file = open(filename, 'r')
    try:
        validity = csv.Sniffer().sniff(csv_file.read(1024))
        csv_file.seek(0)
        return True
    except csv.Error:
        return False
