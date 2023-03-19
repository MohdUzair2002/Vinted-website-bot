import csv
links_all=[]
with open('link_all.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        links_all.append(row)
        print(row)