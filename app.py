from flask import Flask, render_template, request
import re

app = Flask(__name__)

def clean_handle(line):
    # Remove all whitespace and convert to lowercase
    return re.sub(r'\s+', '', line).strip().lower()

def extract_usernames(file_storage):
    usernames = set()
    filename = file_storage.filename.lower()
    if filename.endswith('.pdf'):
        import PyPDF2
        reader = PyPDF2.PdfReader(file_storage)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        lines = text.splitlines()
    else:
        content = file_storage.stream.read().decode('utf-8', errors='ignore')
        lines = content.splitlines()
    for line in lines:
        line = line.strip()
        if line and " " not in line:  # Likely a handle
            usernames.add(clean_handle(line))
    return usernames

@app.route('/', methods=['GET', 'POST'])
def index():
    not_following_back = None
    error = None
    if request.method == 'POST':
        try:
            following_file = request.files['following']
            followers_file = request.files['followers']

            following = extract_usernames(following_file)
            followers = extract_usernames(followers_file)

            not_following_back = sorted(h for h in following if h not in followers)
        except Exception as e:
            error = str(e)
            print("Error:", error)

    return render_template('index.html', not_following_back=not_following_back, error=error)

if __name__ == '__main__':
    app.run(debug=True)



