"""
Created on Wed Oct 23 10:33:50 2019

@author: Nicholas Zomparelli

This code was created by me (Nicholas Zomparelli) in Python 2.7 for the 2019 
Insight Data Engineering Coding Challenge. Below is the entirity of the code, 
commented for convenience. For more details about the code, refer to the README 
file

The code takes in a file named Border_Crossing_Entry_Data.csv and outputs a
file names report.csv
"""

#####IMPORTING DATA###########################################################

""" 
The input .csv file is first imported here using the function csv.reader, 
from the CSV library (a standard Python 2.7 library) and stored in a list

"""

import csv
borderdataraw=[] 

with open('./input/Border_Crossing_Entry_Data.csv') as datafile:
    reader=csv.reader(datafile, delimiter=',')
    for data in reader:
           borderdataraw.append(data)

#The first row of the data containing the headings is removed
borderdata=borderdataraw[1:]


#####DATA EXTRACTION##########################################################

"""
Once the data is imported into a list, it is queried and essential information 
is extracted and stored in separate lists. The information in the lists will 
be queried later on in the code
"""

#Defining lists to store extracted data
Measures=[]
Borders=[]
Months=[]
Years=[]
Dates=[]

#Extracting the data and storing it
for i in range(0,len(borderdata)):
       Measures.append(borderdata[i][5])
       Years.append(borderdata[i][4].split('/')[2].split(' ')[0])
       Borders.append(borderdata[i][3])
       Months.append(borderdata[i][4].split('/')[0])
       Dates.append(borderdata[i][4])


#remove duplicates from lists and sorting     
Measures=list(set(Measures))

Borders=list(set(Borders))

Months=list(set(Months))
Months.sort()

Years=list(set(Years))
Years.sort()

Dates=list(set(Dates))
Dates.sort()


#####MATRIX CREATION AND FILLING##############################################
"""
For each year, the "number of crossings" data is organized into a matrix 
called the DatabaseMatrix, whose dimensions reflect the number of borders, 
measures and months contained in the data.

Thus for datasets containing X number of years of data, there are X number of
DatabaseMatrix matrices, named as DatabaseMatrix['year']
       -#i.e. 1999 border data is stored in DatabaseMatrix['1999']

In addition, two other matrices are created per year, to store the calculations
performed on the data. Their dimensions are copies of the DatabaseMatrix:
       
       -RunningAverageMatrix: 
              holds the running average of border crosses, per border, per 
              month, per measure
       
       -SumMatrix: 
             holds the sum of border crosses, per border, per month, per 
             measure
       
Lastly, the DateMatrix matrix is created (same dimensions as previous) to store
the timestamp associated with each data entry
"""

#Creating a directory of matrices, one for each matrix
DatabaseMatrix={} 
RunningAverageMatrix={}
SumMatrix={}
DateMatrix={}

"""
Creating correctly sized matrices, to be filled later. Dimensions are 
dependant on the number of years of data, number of borders, number of 
measures and number of months
"""
for h in Years:
       DatabaseMatrix[h]=[[],[]]
       RunningAverageMatrix[h]=[[],[]]
       SumMatrix[h]=[[],[]]
       DateMatrix[h]=[[],[]]
             
for h in range(0,len(Years)):       
       for i in range(0,len(Borders)):
              for j in range(0,len(Measures)):
                     DatabaseMatrix[Years[h]][i].append([])
                     RunningAverageMatrix[Years[h]][i].append([])
                     SumMatrix[Years[h]][i].append([])
                     DateMatrix[Years[h]][i].append([])
                     for k in range(0,len(Months)):
                            DatabaseMatrix[Years[h]][i][j].append([])
                            RunningAverageMatrix[Years[h]][i][j].append([])
                            SumMatrix[Years[h]][i][j].append([])
                            DateMatrix[Years[h]][i][j].append([])

                   

#Nesting form of matrices: year --> border --> month --> measure


#Going through border data and extracting information. 
for i in range(0,len(borderdata)):
       b=borderdata[i][3]
       dt=borderdata[i][4]
       month=borderdata[i][4].split('/')[0]
       ts=borderdata[i][4].split('/')
       year=ts[2].split(' ')[0]
       ms=borderdata[i][5]
       value=borderdata[i][6]
       
       
       i_year=Years.index(year)
       i_month=Months.index(month)
       i_border=Borders.index(b)
       i_measure=Measures.index(ms)
       
       
       DatabaseMatrix[Years[i_year]][i_border][i_measure][i_month].append(float(borderdata[i][6]))
       DateMatrix[Years[i_year]][i_border][i_measure][i_month].append(borderdata[i][4])
       
        
#####CALCULATIONS#############################################################
       
"""
Once the DatabaseMatrix is created and filled for each year, calculations for 
the sum of the total number of crossings and running monthly average of total 
crossings can be performed.

Note: Since the SumMatrix data is used to calculate the running average, it 
must be filled first
"""

#Filling the SumMatrix matrices with summed crossing data
for h in range(0,len(Years)):
       for j in range(0,len(Borders)):
              for k in range(0, len(Measures)):
                     for l in range(0, len(Months)):
                            SumMatrix[Years[h]][j][k][l]=sum(DatabaseMatrix[Years[h]][j][k][l])
  
#Filling the RunningAverageMatrix matrices with averaged data                   
for h in range(0,len(Years)):
       for j in range(0,len(Borders)):
              for k in range(0, len(Measures)):
                     RunningAverageMatrix[Years[h]][j][k][0]=0.0
                     for l in range(1, len(Months)):
                            RunningAverageMatrix[Years[h]][j][k][l]=round(sum(SumMatrix[Years[h]][j][k][0:l])/float(l))                   
              

#####COLLECTING AND COMPILING CALCULATED DATA#################################

"""
As of this point, the calculation results are scattared (but in order) over the 
three matrices. Thus in order to generate an output file, the calculated data
must be collected into a single output list
"""

#Creating Output file
outputraw=[]
for h in range(0,len(Years)):
       for l in range(0,len(Months)):
              for m in range(0,len(Borders)):
                     for n in range(0,len(Measures)):
                   
                            if len(DateMatrix[Years[h]][m][n][l])!=0: 
                                   outputraw.append([Borders[m],DateMatrix[Years[h]][m][n][l][0],Measures[n],SumMatrix[Years[h]][m][n][l],RunningAverageMatrix[Years[h]][m][n][l]])
                                   
                            else:
                                   pass                            
                         
"""
Some DateMatrix entries contain points with no data. This above if condition 
removes them on the basis that every data point has an associated date (i.e. 
the length of that specific entry in the DataMatrix is not equal to zero)
"""


#####SORTING OUTPUTTED DATA###################################################
                                   
"""
A requirement of the outputted data is that it is organized in descending order
by date, value, measure and border
"""

#arranging the data by decreasing data by flipping the list
outputraw=outputraw[::-1]

"""
At this point the data is sorted by date, but not by value. The following loop 
takes sections of entries of the output list that have the same timestamp and
rearranges them from largest to smallest value. It then puts the rearraged 
section back into its original index range location in the list
"""
for i in range(0,len(Dates)):
       indices=[]
       for j in range(0,len(outputraw)):
              if outputraw[j][1]==Dates[i]:
                     indices.append(j)
              
              else:
                     pass
              
       #Dates that only have one data entry value associated with in need not 
       #be sorted     
       
       if len(indices)>1:       
              tempdata=[]
              for k in range(0,len(indices)):
                     tempdata.append(outputraw[indices[k]])
                     
              tempdata.sort(key=lambda x: x[3], reverse=True)
                     
                     
              outputraw[indices[0]:(indices[len(indices)-1]+1)]=tempdata   
       
       else:
              pass


#####OUTPUTTING THE DATA######################################################
"""
The outputted report.csv file is generated using the csv.writer from the csv
library
"""

#Attaching a header to the data     
output=[['Border', 'Date', 'Measure', 'Value', 'Average']]+outputraw

#Writing the output file
with open("./output/report.csv", "wb") as rep:
    writer = csv.writer(rep)
    writer.writerows(output)
