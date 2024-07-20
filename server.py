from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import nbformat as nbf

app = Flask(__name__)

def scrape_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = "\n".join(para.get_text() for para in paragraphs)
        return text
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"

def update_notebook(text):
    notebook_path = "summarise.ipynb"
    with open(notebook_path) as f:
        nb = nbf.read(f, as_version=4)
    
    text_found = False
    for cell in nb['cells']:
        if cell['cell_type'] == 'code' and 'text = ' in cell['source']:
            cell['source'] = f'text = """{text}"""'
            text_found = True
            break
    
    if not text_found:
        # Create a new cell with the text variable if not found
        new_cell = nbf.v4.new_code_cell(source=f'text = """{text}"""')
        nb['cells'].insert(0, new_cell)
    
    with open(notebook_path, 'w') as f:
        nbf.write(nb, f)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    url = data.get('url')
    if url:
        text = scrape_website(url)
        update_notebook(text)
        return jsonify({"status": "success", "text": text}), 200
    else:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

if __name__ == "__main__":
    app.run(debug=True)
