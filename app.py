import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import urllib3
import streamlit as st

# Suppress only the single InsecureRequestWarning from urllib3 needed for certificate errors
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Streamlit app
st.title("CSS Font-Face Extractor")

# Step 1: URL to be entered by user
url = st.text_input("Enter the URL:")

if url:
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an error for bad status codes

        # Step 2: Parse the HTML to extract CSS content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Function to fetch and append CSS content
        def fetch_css_content(css_url, base_url):
            full_url = urljoin(base_url, css_url)
            try:
                css_response = requests.get(full_url, verify=False)
                css_response.raise_for_status()  # Raise an error for bad status codes
                return css_response.text, full_url
            except requests.exceptions.RequestException as e:
                st.warning(f"Failed to fetch CSS content from {full_url}. Error: {e}")
                return '', full_url

        # Collect CSS from linked CSS files
        css_sources = []
        css_files = []  # List to keep track of the names of CSS files
        link_tags = soup.find_all('link', rel='stylesheet')
        for tag in link_tags:
            css_url = tag['href']
            css_content, source = fetch_css_content(css_url, base_url=url)
            if css_content:
                css_sources.append((css_content, source))
                css_files.append(css_url.split('/')[-1])  # Add the file name to the list

        # Step 3: Extract @font-face blocks and their sources
        font_faces = []
        for css_content, source in css_sources:
            font_face_blocks = re.findall(r'@font-face\s*{[^}]+}', css_content)
            for block in font_face_blocks:
                properties = re.findall(r'(\w[\w-]*):\s*([^;]+);', block)
                font_face_dict = {'source': source}
                for prop, value in properties:
                    if prop == 'font-family':
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]  # Remove double quotes
                        font_face_dict['font-family'] = value
                    if prop == 'src':
                        font_face_dict['src'] = value
                font_faces.append(font_face_dict)

        # Step 4: Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(font_faces)

        # Step 5: Display the DataFrame
        st.subheader("Font-Face Declarations")
        st.dataframe(df)

        # Step 6: Display the list of CSS files considered
        st.subheader("CSS files considered")
        for css_file in css_files:
            st.write(css_file)

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL: {e}")
