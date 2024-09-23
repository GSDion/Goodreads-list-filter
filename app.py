import os
from flask import Flask, request, render_template, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Home route to display the form and results
@app.route('/', methods=['GET', 'POST'])
def index():
    table = None  # Initialize the variable to store the filtered table
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded", 400

        file = request.files['file']
        
        if file.filename == '':
            return "No selected file", 400
        
        if file:
            # Load the uploaded file directly into a DataFrame (in-memory)
            dataFrame = pd.read_csv(file)

            # Get the filter inputs from the form
            # TO DO: Populate filters on form depending on column names of csv file
            # TO DO: Multiple filters (one sub_filter each)
            filters = {}
            filter_type = request.form.get('filter_type')
            sub_filter = request.form.get('sub_filter')
            
            if filter_type and sub_filter:
                filters[filter_type] = sub_filter
            
            # Apply filters
            filtered_data = filter_dataframe(dataFrame, filters)

            # Convert filtered DataFrame to HTML table
            table = filtered_data.to_html(classes='table table-striped', index=False)

    # Render the form and the results on the same page/below the form
    return render_template('index.html', table=table)

# Function to apply multiple filters
def filter_dataframe(dataFrame, filters):
    for column_name, sub_filter in filters.items():
        if column_name in ['Year Published', 'Date Added']:
            dataFrame = dataFrame[dataFrame[column_name].astype('str').str.contains(sub_filter, na=False)]
        else:
            dataFrame = dataFrame[dataFrame[column_name].str.contains(sub_filter, na=False)]
    return dataFrame

if __name__ == '__main__':
    app.run(debug=True)
