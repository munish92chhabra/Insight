import csv            #reading data from csv input file and converting to different lists for each column of input data
f = open('login.csv')
csv_f = csv.reader(f)

ip_list = []
date_list =[]
time_list = []
cik_list = []
accession_list = []
extension_list = []

for row in csv_f:    
    ip_list.append(row[0])
    date_list.append(row[1])
    time_list.append(row[2])
    cik_list.append(row[3])
    accession_list.append(row[4])
    extension_list.append(row[5])

ip_list.pop(0) #removing the first element of the list
date_list.pop(0)
time_list.pop(0)
cik_list.pop(0)
accession_list.pop(0)
extension_list.pop(0)

in_file = open("inactivity_period.txt", "rt") #getting information of the inactivity period 
contents = in_file.read()         
in_file.close()
inactivity_period = int(contents)

time_list2 = [0]*len(time_list)

for  i in range(len(time_list2)):   #converting h:mm:ss to ss
    time_list_int = list(time_list[i])
    time_in_hrspart = int(time_list_int[0])
    time_in_minpart = 10*int(time_list_int[2])+ int(time_list_int[3])
    time_in_secondpart = 10*int(time_list_int[5])+ int(time_list_int[6])
    time_list2[i] = 3600*time_in_hrspart + 60* time_in_minpart + time_in_secondpart
    
#organizing data obtained of each second into different list of tables    
counter = list(set(time_list2))

dimension_x = len(counter)
dimension_y = len(ip_list)
dimension_z = 6

#creating 3D list of lists
data_in_second = []
data_in_second = [[[None for _ in range(dimension_z)] for _ in range(dimension_y)] for _ in range(dimension_x)]

#Reading from the input file login.csv and separating the data for each second into different table
for j in range(dimension_x):
    for i in range(dimension_y):
        if time_list2[i] == counter[j]:
            data_in_second[j][i] = [ip_list[i], date_list[i], time_list[i], cik_list[i],accession_list[i],extension_list[i]]
            
            
#creating a table for document requested by the user containing ip number and the number of document requested
dimension_z1 = 1
document_requested_in_second = []
document_requested_in_second = [[[None for _ in range(dimension_z1)] for _ in range(dimension_y)] for _ in range(dimension_x)]

for i in range(dimension_x):
    for j in range(dimension_y):
            document_requested_in_second[i][j][0] = data_in_second[i][j][0]

dimension_z2 = 2
document_frequency_in_second = []
document_frequency_in_second = [[[None for _ in range(dimension_z2)] for _ in range(dimension_y)] for _ in range(dimension_x)]
frequency = []

for i in range(dimension_x):
    for j in range(dimension_y):
        if document_requested_in_second[i][j] != document_requested_in_second[i][j-1]:
            temp=document_requested_in_second[i][j]
            frequency=document_requested_in_second[i].count(temp)
            if temp != None:
                document_frequency_in_second[i][j][0]=temp
                document_frequency_in_second[i][j][1]=frequency


dimension_x3 = len(document_frequency_in_second)
dimension_y3 = len(document_frequency_in_second[0])
dimension_z3 = len(document_frequency_in_second[0][0])

output =[[None for _ in range(7)] for _ in range(6)]

#data for first session of inactivity period


for i in range(dimension_y):
    for k in range(dimension_x):
        if time_list2[i] == k:
            for j in range(dimension_x):
                if ip_list[i] == document_requested_in_second[k][j][0]:
                    if document_frequency_in_second[k][j][1] == 1:
                        output[k] = [ data_in_second[k][j][0], data_in_second[k][j][1], data_in_second[k][j][2], data_in_second[k][j][1], data_in_second[k][j][2], 1, document_frequency_in_second[k][j][1]  ]
                        

print output

import csv
with open('output.txt', 'wb') as f:
    wtr = csv.writer(f, delimiter= ' ')
    wtr.writerows(output)

with open('output.txt', 'r') as f:
    for line in f:
        print line,
