import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash
import pyttsx3
import PyPDF2
from threading import Thread
from werkzeug.utils import secure_filename
from PyPDF2.errors import DependencyError
import time

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'

# Initialize pyttsx3 engine globally
engine = pyttsx3.init()

# Directory to store uploaded PDFs
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database setup
DATABASE = 'pdf.db'

# Global variable to store paused state
paused = False
current_sentence = 0
text_sentences = []


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pdf_files (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filename TEXT,
                        filepath TEXT
                      )''')
    conn.commit()
    conn.close()


# Function to save PDF file information to the database
def save_pdf_to_db(filename, filepath):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pdf_files (filename, filepath) VALUES (?, ?)", (filename, filepath))
    conn.commit()
    conn.close()


# Function to retrieve all converted PDFs from the database
def get_all_pdfs():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, filepath FROM pdf_files")
    result = cursor.fetchall()
    conn.close()
    return result


# Function to convert PDF to text from a specific page
def extract_text_from_pdf(pdf_file_path, start_page):
    with open(pdf_file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""

        if reader.is_encrypted:
            try:
                reader.decrypt('')  # Modify with password if needed
            except DependencyError:
                return "This PDF file is encrypted and cannot be processed without PyCryptodome."

        for page_num in range(start_page - 1, len(reader.pages)):
            text += reader.pages[page_num].extract_text()

        return text


# Function to handle text-to-speech in chunks
# Function to handle text-to-speech in chunks
def text_to_speech_chunked(voice, rate, volume):
    global engine, paused, current_sentence, text_sentences

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id if voice == 'female' else voices[0].id)
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    while current_sentence < len(text_sentences):
        # Pause check before speaking
        while paused:
            time.sleep(0.1)  # Small delay to avoid CPU overconsumption

        sentence = text_sentences[current_sentence]
        engine.say(sentence)
        engine.runAndWait()
        current_sentence += 1
        time.sleep(0.2)  # Add small delay between sentences


@app.route('/', methods=['GET', 'POST'])
def index():
    global paused, current_sentence, text_sentences

    # Fetch all previously converted PDFs
    pdf_list = get_all_pdfs()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'convert':
            paused = False
            current_sentence = 0
            text_sentences = []

            pdf_file = request.files.get('pdf')
            if not pdf_file:
                return "No file selected. Please choose a file to convert."

            voice = request.form['voice']
            rate = int(request.form['rate'])
            volume = float(request.form['volume'])
            start_page = int(request.form['start_page'])

            filename = secure_filename(pdf_file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            pdf_file.save(filepath)

            save_pdf_to_db(filename, filepath)
            session['pdf_file_path'] = filepath

            text = extract_text_from_pdf(filepath, start_page)
            text_sentences = text.split(". ")

            # Start new thread for text-to-speech
            tts_thread = Thread(target=text_to_speech_chunked, args=(voice, rate, volume))
            tts_thread.start()

        elif action == 'pause':
            paused = True

        elif action == 'resume':
            paused = False  # Unpause the process
            voice = request.form['voice']
            rate = int(request.form['rate'])
            volume = float(request.form['volume'])

            # Resume the same thread
            tts_thread = Thread(target=text_to_speech_chunked, args=(voice, rate, volume))
            tts_thread.start()

        return redirect(url_for('index'))

    return render_template('index.html', pdf_list=pdf_list)


@app.route('/view_pdf/<int:pdf_id>', methods=['GET'])
def view_pdf(pdf_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT filename, filepath FROM pdf_files WHERE id=?", (pdf_id,))
    pdf = cursor.fetchone()
    conn.close()

    if pdf:
        filename, filepath = pdf
        return render_template('view_pdf.html', filename=filename, filepath=filepath)
    else:
        return "PDF not found", 404


# Route to handle deleting a PDF
@app.route('/delete_pdf/<int:pdf_id>', methods=['POST'])
def delete_pdf(pdf_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Get the file path before deleting
    cursor.execute("SELECT filepath FROM pdf_files WHERE id = ?", (pdf_id,))
    result = cursor.fetchone()

    if result:
        filepath = result[0]

        # Delete the file from the server
        if os.path.exists(filepath):
            os.remove(filepath)

        # Delete the entry from the database
        cursor.execute("DELETE FROM pdf_files WHERE id = ?", (pdf_id,))
        conn.commit()

    conn.close()

    flash('PDF file has been deleted successfully!', 'success')
    return redirect(url_for('index'))


# Route to download the actual PDF file
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)