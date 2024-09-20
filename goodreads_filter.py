import os
import pandas as pd
# from tabulate import tabulate

"""Book Id                         int64
Title                          object
Author                         object
Author l-f                     object
Additional Authors             object
ISBN                           object
ISBN13                         object
My Rating                       int64
Average Rating                float64
Publisher                      object
Binding                        object
Number of Pages                 int64
Year Published                  int64
Original Publication Year     float64
Date Read                      object
Date Added                     object
Bookshelves                    object
Bookshelves with positions     object
Exclusive Shelf                object
My Review                      object
Spoiler                       float64
Private Notes                 float64
Read Count                      int64
Owned Copies                    int64
dtype: object"""

pd.set_option('display.max_columns', None)

## NOT APPLICABLE
def filter_genre(dataFrame, sub_filter):
    dataFrame = dataFrame[dataFrame['Genre'].str.contains(sub_filter,na=False)]
    print("\nFetching rows with {0:s}.....\n".format(sub_filter))
    # dataFrame.style
    # print(tabulate(dataFrame, headers = 'keys', tablefmt='psql'))
    print(dataFrame)

## WORKING
def  filter_author(dataFrame, sub_filter):
    dataFrame = dataFrame[dataFrame['Author'].str.contains(sub_filter,na=False)]
    print("\nFetching rows with {0:s}.....\n".format(sub_filter))
    print(dataFrame)

# WORKING
#AttributeError: Can only use .str accessor with string values!. Did you mean: 'std'?
def filter_year_published(dataFrame, sub_filter):
    dataFrame = dataFrame[dataFrame['Year Published'].astype('str').str.contains(sub_filter,na=False)]
    print("\nFetching rows with {0:s}.....\n".format(sub_filter))
    print(dataFrame)


# WORKING
#ValueError: Cannot mask with non-boolean array containing NA / NaN values
def filter_publisher(dataFrame, sub_filter):
    dataFrame = dataFrame[dataFrame['Publisher'].str.contains(sub_filter,na=False)]
    print("\nFetching rows with {0:s}.....\n".format(sub_filter))
    print(dataFrame)

# WORKING
def filter_binding_type(dataFrame, sub_filter):
    dataFrame = dataFrame[dataFrame['Binding'].str.contains(sub_filter,na=False)]
    print("\nFetching rows with {0:s}.....\n".format(sub_filter))
    print(dataFrame)

## NOT WORKING
def filter_date_added(dataFrame, sub_filter):
    # dataFrame = dataFrame[dataFrame['Date Added'].astype('str').str.contains(sub_filter,na=False)]
    dataFrame = dataFrame[dataFrame['Date Added'].isin(sub_filter)]
    print("\nFetching rows with {0:s}.....\n".format(sub_filter))
    print(dataFrame)

"""Potential Filters: Author l-f, Additional Authors, ISBN, ISBN13, My Rating, Average Rating,
    Original Publication Year,Read Count,Owned Copies, My Review (search for keywords)"""

## Console to prompt user
# Ask for file name
fileName = input("Enter your file name: ")

# If file name in current directory, then open
homePath = './'
fullPath = homePath + fileName
if os.path.exists(fullPath):
    dataFrame = pd.read_csv(fileName)

# Ask for filter(s), (One filter for now)
print(dataFrame.dtypes)
filter = input("Enter the type of filter that you would like to use: ")
sub_filter = input("Enter the constraint for the filter: ") # Make the sub-filter case insensitive
# Call methods based on user input 
# Make these case insensitive
match filter:
    case "genre":
        filter_genre(dataFrame, sub_filter)
    case "author":
        filter_author(dataFrame, sub_filter)
    case "year published":
        filter_year_published(dataFrame,sub_filter)
    case "publisher":
        filter_publisher(dataFrame,sub_filter)
    case "binding type":
        filter_binding_type(dataFrame,sub_filter)
    case "date added":
        filter_date_added(dataFrame, sub_filter)
    

