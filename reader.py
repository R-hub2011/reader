import pytesseract
from PIL import Image
from transformers import pipeline
import streamlit as st

# Function to extract text from the image
def extract_text(image_path):
    try:
        # Open the image file
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

# Function to solve problems using Hugging Face Transformers
def solve_problem(problem_text):
    try:
        # Load a pre-trained model from Hugging Face
        model = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")
        response = model(
            f"Explain and solve the following problem:\n{problem_text}",
            max_length=500,
            truncation=True
        )
        return response[0]['generated_text']
    except Exception as e:
        return f"Error solving problem: {str(e)}"

# Streamlit Web Interface
def main():
    st.title("AI Problem Solver")
    st.write("Upload a screenshot, and the tool will extract the problem and solve it!")

    uploaded_file = st.file_uploader("Upload a Screenshot", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        # Display uploaded image
        st.image(uploaded_file, caption="Uploaded Screenshot", use_column_width=True)

        # Extract text
        extracted_text = extract_text(uploaded_file)
        st.text_area("Extracted Problem Text", extracted_text)

        # Solve problem
        if st.button("Solve"):
            solution = solve_problem(extracted_text)
            st.text_area("Solution", solution)

if __name__ == "__main__":
    main()