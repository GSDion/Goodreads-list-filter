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
"""Potential Filters: Author l-f, Additional Authors, ISBN, ISBN13, My Rating, Average Rating,
    Original Publication Year,Read Count,Owned Copies, My Review (search for keywords)"""

# Implemented and working: Author, Year Published, Binding, Publisher
# Not working: date added
# Not applicable atm: Genre
# Year Published Error - AttributeError: Can only use .str accessor with string values!. Did you mean: 'std'?
# Publisher Error -  ValueError: Cannot mask with non-boolean array containing NA / NaN values

pd.set_option('display.max_columns', None)

# General filter method
def filter_dataframe(dataFrame, filters):
    # Loop through all filters provided
    for column_name, sub_filter in filters.items():
        # Attempt to convert columns to string before applying the filter
        if column_name in ['Year Published', 'Date Added']:  # Columns that might need specific handling
            # Dated added YYYY/MM/DD
            dataFrame = dataFrame[dataFrame[column_name].astype('str').str.contains(sub_filter, na=False)]
        else:
            dataFrame = dataFrame[dataFrame[column_name].str.contains(sub_filter, na=False)]
        
        print("\nFetching rows with '{0:s}' in column '{1:s}'.....".format(sub_filter, column_name))
    
    # Return the filtered DataFrame
    print(dataFrame)
    return dataFrame
    
## NOT APPLICABLE
def filter_genre(dataFrame, sub_filter):
    dataFrame = dataFrame[dataFrame['Genre'].str.contains(sub_filter,na=False)]
    print("\nFetching rows with {0:s}.....\n".format(sub_filter))
    # dataFrame.style
    # print(tabulate(dataFrame, headers = 'keys', tablefmt='psql'))
    print(dataFrame)

## NOT WORKING
def filter_date_added(dataFrame, sub_filter):
    # dataFrame = dataFrame[dataFrame['Date Added'].astype('str').str.contains(sub_filter,na=False)]
    dataFrame = dataFrame[dataFrame['Date Added'].isin(sub_filter)]
    print("\nFetching rows with {0:s}.....\n".format(sub_filter))
    print(dataFrame)

## Console to prompt user
# Ask for file name
fileName = input("Enter your file name: ")

# If file name in current directory, then open
homePath = './'
fullPath = homePath + fileName
if os.path.exists(fullPath):
    dataFrame = pd.read_csv(fileName)


print(dataFrame.dtypes)

# Initialize a dictionary to store multiple filters
filters = {}
# Map filter types to column names in the DataFrame
column_mapping = {
    "genre": "Genre",
    "author": "Author",
    "year published": "Year Published",
    "publisher": "Publisher",
    "binding": "Binding",
    "date added": "Date Added"
}

while True:
    # Ask for filter type
    filter_type = input("Enter the type of filter (genre, author, year published, publisher, binding type, date added), or type 'done' to finish: ").lower()
    
    if filter_type == 'done':
        break  # Exit the loop when user is done adding filters

    if filter_type in column_mapping:
        sub_filter = input(f"Enter the constraint for the '{filter_type}' filter: ")
        filters[column_mapping[filter_type]] = sub_filter  # Add filter to the dictionary
    else:
        print("Invalid filter type entered.")

# # Ensure the filter type exists in the mapping
# if filter_type in column_mapping:
#     filter_dataframe(dataFrame, column_mapping[filter_type], sub_filter)
# else:
#     print("Invalid filter type entered.")

# Apply all filters
if filters:
    filtered_data = filter_dataframe(dataFrame, filters)
else:
    print("No filters applied.")