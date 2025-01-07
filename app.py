import os
from flask import Flask, request, render_template, redirect, url_for, session
# The Session instance is not used for direct access, should always use flask.session instead
from flask_session import Session
import pandas as pd
from config import Config

ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER']
app.config["SECRET_KEY"]
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# FAQ/Contact Route
@app.route('/faq')
def faq():
    return render_template('faq.html')

# Home route to display the form and results
@app.route('/', methods=['GET', 'POST'])
def index():
    table = None
    uploaded_file_name = session.get('uploaded_file')  # Retrieve the file name from session
    
    # Check if a file has been uploaded and saved previously
    if uploaded_file_name:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file_name)
    else:
        file_path = None
    
    if request.method == 'POST':
        # Debug: Print the entire form data
        print("Form data received:", request.form)
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '':
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                # Store only the filename in the session so as to save space (cookies can only store so much)
                session['uploaded_file'] = file.filename 

            # If file_path is None, prompt the user to upload a file
            if not file_path or not os.path.exists(file_path):
                return "No file uploaded or found. Please upload a file.", 400
        
            # Load the uploaded file directly into a DataFrame (in-memory)
            dataFrame = pd.read_csv(file_path)
            filter_types = request.form.getlist('filter_type[]')
            sub_filters = request.form.getlist('sub_filter[]')
            # Debug: Print filters
            print("Filter types:", filter_types)
            print("Sub filters:", sub_filters)
            # Build the filters dictionary
            filters = {}
            for filter_type, sub_filter in zip(filter_types, sub_filters):
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
        print(f"Filtering column '{column_name}' with constraint '{sub_filter}'")
        if column_name not in dataFrame.columns:
                print(f"Column '{column_name}' does not exist in the DataFrame. Skipping...")
                continue  # Skip filters for non-existent columns
        try:
            if column_name in ['Year Published', 'Date Added']:
                dataFrame = dataFrame[dataFrame[column_name].astype('str').str.contains(sub_filter, na=False, case=False)]
            else:
                dataFrame = dataFrame[dataFrame[column_name].str.contains(sub_filter, na=False, case=False)]
                print(f"DataFrame after filtering '{column_name}':\n", dataFrame)
        except Exception as e:
            print(f"Error filtering column '{column_name}': {e}")
    return dataFrame

if __name__ == '__main__':
    app.run(debug=True)
