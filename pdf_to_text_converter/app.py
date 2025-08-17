import PyPDF2
import pyttsx3

# Initialize the speech engine
engine = pyttsx3.init()


def pdf_to_text(pdf_file):
    # Open the PDF file
    with open(pdf_file, 'rb') as file:
        # Create PDF reader object
        reader = PyPDF2.PdfReader(file)

        # Extract text from each page
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()

    return text


def text_to_speech(text):
    engine.say(text)  # Convert text to speech
    engine.runAndWait()  # Wait for the speech to finish


def convert_pdf_to_speech(pdf_file):
    text = pdf_to_text(pdf_file)  # Extract text from the PDF
    text_to_speech(text)  # Convert text to speech


# File path to the PDF
pdf_file = 'ACMP 271 Data Communication and Networks E-Contents.pdf'  # Replace with the path to your PDF file

convert_pdf_to_speech(pdf_file)
