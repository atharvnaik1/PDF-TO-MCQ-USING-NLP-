import streamlit as st
import random
import PyPDF2
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def reading_pdf(pdf):
    with open(pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        context = ''
        for i in reader.pages:
            context += i.extract_text()
        return context


def get_mca_questions(context: str, num_questions: int):

# Process the extracted text with spaCy.
    doc = nlp(context)


    def generate_mcq_with_multiple_answers(question, correct_answers, other_options, num_options=4):
        options = correct_answers + other_options
        random.shuffle(options)

        mcq = {
            "question": question,
            "options": options,
            "correct_answers": correct_answers
        }

        return mcq

    def generate_question():
#Spacy's doc property used to iterate over the sentences in a particular document.
        sentence = random.choice(list(doc.sents))
        blank_word = random.choice([token for token in sentence if not token.is_punct])

        question_text = sentence.text.replace(blank_word.text, "____")
# Fill the blank with correct_answers
        correct_answers = [blank_word.text]

        other_options = [token.text for token in doc if token.is_alpha and token.text != correct_answers[0]]
# Generate multiple solutions.
        # num_correct_options = random.randint(1,1)
        # correct_answers += random.sample(other_options, num_correct_options)

        # num_other_options = min(4 - num_correct_options-1, len(other_options))
        num_other_options = min(4 - 1, len(other_options))

        other_options = random.sample(other_options, num_other_options)

        mcq = generate_mcq_with_multiple_answers(question_text, correct_answers, other_options)
        return mcq


    questions = [generate_question() for _ in range(num_questions)]

    mca_questions = []
    for i, question in enumerate(questions, start=1):
        quest_text = f"Q{i}: {question['question']}\n"
        options_text = ""
        for j, option in enumerate(question['options']):
            options_text += f"{j+1}. {option}\n"
# Ordinal characters gives unicode converted in character using chr.
        get_correct_options = " & ".join([f"({chr(ord('a')+question['options'].index(ans))})" for ans in question['correct_answers']])
        correct_options_text = f"\n Correct Option: {get_correct_options}"

        mca_question = f"{quest_text}{options_text}{correct_options_text}\n"
        mca_questions.append(mca_question)

    return mca_questions

st.write(
    """
    <style>
     /* Hide the close button */
    .sidebar .stSidebarClose {
        display: none;
    }

    /* Make the sidebar sticky */
    .sidebar .sidebar-content {
        position: -webkit-sticky;
        position: sticky;
        top: 0;
        height: 100vh; /* Adjust the height as needed */
        overflow-y: auto; /* Allow scrolling if the content is taller than the screen */
    }
    body {
        font-family: 'Arial', sans-serif;
        background-color: #F4BBFF; /* Background color for the entire app */
    }
    #  .stApp {
    
    #      background-color: #dbe4f7;
    # }
    .streamlit-title {
        font-size: 36px;
        color: black; /* Primary color for the title */
        padding: 20px 0;
        text-align: center;
    }
    
    button border color when selected */
    }
    .stButton {
        background-color: #007BFF; /* Button background color */
        color: black; /* Button text color */
        padding: 10px 20px;
        border: none;
    }
    
    
    </style>
    """,
    unsafe_allow_html=True
)

# [theme]
# primaryColor="#d29bf9"
# backgroundColor="#dbe4f7"
# secondaryBackgroundColor="#bfd1f3"
# textColor="#3f3131"


#   Define the Streamlit app
def main():
    icon_url = "file:///E:/nlp-mcq/icon.png"
    st.markdown(f'<div style="text-align:center"><img src="{icon_url}"></div>', unsafe_allow_html=True)
    
    st.title("PDF to Multiple-Choice Questions Generator using NLP")

    st.sidebar.header("Sections")


    selected_section = st.sidebar.radio("Select Section", ["🏠 EXTRACTED_TEXT", "📝 Generate Questions"])

    if selected_section == "📝 Generate Questions":
        num_questions = st.number_input("Enter the number of questions:", min_value=1, value=5, step=1)

        chapter_paths = ['E:\\nlp-mcq/chapter-2.pdf', 'E:\\nlp-mcq/chapter-3.pdf', 'E:\\nlp-mcq/chapter-4.pdf']
        selected_chapter = st.selectbox("Select a chapter", chapter_paths)

        if st.button("Generate Questions"):
            chapter_text = reading_pdf(selected_chapter)
            mca_questions = get_mca_questions(chapter_text, num_questions)

            for i, question in enumerate(mca_questions, start=1):
                st.write(f" {question}")

    if selected_section == "🏠 EXTRACTED_TEXT":
        st.subheader("Chapter Context:")
        chapter_paths = ['E:\\nlp-mcq/chapter-2.pdf', 'E:\\nlp-mcq/chapter-3.pdf', 'E:\\nlp-mcq/chapter-4.pdf']
        selected_chapter = st.selectbox("Select a chapter", chapter_paths)
        chapter_text = reading_pdf(selected_chapter)
        st.write(chapter_text)

if __name__ == "__main__":
    main()
