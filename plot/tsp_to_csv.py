import csv
from math import ceil

with open('ja9847.tsp', 'r') as tsp_file:

    reader = tsp_file.readlines()

    csv_file = open('ja9847.csv', 'w')

    writer = csv.DictWriter(csv_file, fieldnames=['id', 'x', 'y'])

    writer.writeheader()

    for row in reader[7:-1]:
        line = row.strip().split()
        writer.writerow({'id': int(line[0]), 'x': ceil(float(line[1])), 'y': ceil(float(line[2]))})
    
    csv_file.close()
        