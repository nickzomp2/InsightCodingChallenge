2019 Insight Data Engineering Coding Challenge Submission by Nicholas Zomparelli


The program "us_border_data_analysis.py" was written by me (Nicholas Zomparelli) for the 2019 Insight Data Engineering Coding Challenge. It is written in Python 2.7 and takes inputted border data and calculates the total number of times the US borders (Mexican and Canadian) are crossed for various measures (vehicles, pedestrians, etc.) as well as the running monthly average of total border crossings for various measures.

In short, the aforementioned code takes in border data and stores the information in various matrices. These matrices are then queried to extract data to calculate the aforementioned sum and running average values, before returning the information is the requested form.

The code is fully scalable to larger datasets and is beneficial in the fact that the matrices act as databases for the border data, which can be queried if need be. Aside from built-in Python 2.7 functions, the only library that was used was csv, to handle the inputting and outputting of data. It should be noted that the csv library is a Python 2.7 standard library however.
