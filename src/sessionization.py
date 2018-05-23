import csv

f = open('Insight/input/login.csv')
csv_f = csv.reader(f)

for row in csv_f:
  print row
