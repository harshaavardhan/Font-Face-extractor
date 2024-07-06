
# CSS Font-Face Extractor

This is a Streamlit application that extracts and displays `@font-face` declarations from the CSS files of a given URL. It lists the `font-family` and `src` properties for each `@font-face` declaration and shows the names of the CSS files considered.

## Features

- Input a URL to analyze
- Extract and display `@font-face` declarations from CSS files
- List the `font-family` and `src` properties for each `@font-face` declaration
- Display the names of the CSS files considered

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/css-font-face-extractor.git
   cd css-font-face-extractor

2. Install the required dependencies:
   pip install -r requirements.txt

## Usage
Run the Streamlit app. Open cmd on path of the py file and run the below command

streamlit run app.py

Open your web browser and go to http://localhost:8501.

1) Enter the URL you want to analyze in the input field and press Enter.

2) The app will display the @font-face declarations in a table and list the CSS files considered.

Error Handling
SSL self-signed certificate errors are handled.
If the URL does not respond or does not allow scraping, an appropriate error message is displayed.
