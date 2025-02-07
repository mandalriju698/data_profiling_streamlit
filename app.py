import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import sys
import os

# Set the page configuration
st.set_page_config(page_title='Data Profiler', layout='wide')


# Function to get the file size in MB
def get_filesize(file):
    size_bytes = sys.getsizeof(file)
    size_mb = size_bytes / (1024 ** 2)  # Convert bytes to MB
    return size_mb


# Function to validate the file extension
def validate_file(file):
    filename = file.name
    _, ext = os.path.splitext(filename)
    if ext in ('.csv', '.xlsx'):
        return ext
    return False


# Sidebar for file upload and options
with st.sidebar:
    uploaded_file = st.file_uploader("Upload a .csv or .xlsx file (not exceeding 10 MB)")
    if uploaded_file is not None:
        st.write('Modes of Operation:')
        minimal = st.checkbox('Generate minimal report?')
        display_mode = st.radio('Select display mode:', options=('Primary', 'Dark', 'Orange'))

        # Determine the selected display mode
        dark_mode = display_mode == 'Dark'
        orange_mode = display_mode == 'Orange'

# If the user has uploaded a file
if uploaded_file is not None:
    # Validate the file format
    ext = validate_file(uploaded_file)

    if ext:
        # Check the file size
        filesize = get_filesize(uploaded_file)
        if filesize <= 10:  # Check if the file size is within the limit
            # Load the data based on the file type
            if ext == '.csv':
                df = pd.read_csv(uploaded_file)
            else:
                xl_file = pd.ExcelFile(uploaded_file)
                sheet_name = st.sidebar.selectbox('Select the sheet', xl_file.sheet_names)
                df = xl_file.parse(sheet_name)

            # Generate the profile report
            with st.spinner('Generating report...'):
                pr = ProfileReport(df, minimal=minimal)

            # Display the report using Streamlit's Pandas Profiling
            st_profile_report(pr)

        else:
            st.error(f'Maximum allowed file size is 10 MB. Your file is {filesize:.2f} MB.')
    else:
        st.error('Please upload a .csv or .xlsx file.')

else:
    st.title('Data Profiler')
    st.info('Upload your data file in the sidebar to generate a profiling report.')
