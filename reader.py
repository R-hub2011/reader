import pytesseract
import cv2
import openai
from PIL import Image

# Set up Tesseract path if necessary (if you're on Windows, specify the location of Tesseract)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Your OpenAI API Key (replace with your actual API key)
openai.api_key = 'your_openai_api_key_here'


# Function to capture the text from the image or screen
def capture_text_from_image(image_path):
    # Load the image from the specified path
    img = cv2.imread(image_path)
    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply OCR to extract text from the image
    text = pytesseract.image_to_string(gray_img)
    return text


# Function to generate code for the given problem description
def generate_code_from_description(problem_description):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",  # Use the appropriate model for code generation
        prompt=f"Given the following problem description, generate a Python solution code:\n{problem_description}",
        max_tokens=150,
        temperature=0.5
    )
    return response.choices[0].text.strip()


# Main function
def main():
    image_path = input("Enter the image path with the problem statement: ")

    # Step 1: Capture the problem description from the image
    problem_description = capture_text_from_image(image_path)

    # Step 2: Print the captured problem description
    print("Captured Problem Description:")
    print(problem_description)

    # Step 3: Generate Python code based on the problem description
    print("\nGenerating Python solution code...\n")
    solution_code = generate_code_from_description(problem_description)

    # Step 4: Display the generated Python code (the solution)
    print("Generated Python Code:\n")
    print(solution_code)


if __name__ == "__main__":
    main()
