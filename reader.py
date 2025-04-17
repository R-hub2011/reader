import pytesseract
from PIL import Image
import pyautogui
from transformers import pipeline
import time

# Set the path to Tesseract (adjust for your OS and installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows path, adjust if needed

openai.api_key = 'your_openai_api_key_here'


# Function to capture a screenshot of a specific region of the screen
def capture_screen(region=(0, 0, 800, 600)):
    """
    Capture the screen or a specific region and return the image path.
    """
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save("screenshot.png")
    return "screenshot.png"


# Function to extract text from an image using pytesseract (OCR)
def extract_text_from_image(image_path):
    """
    Extract text from the provided image using pytesseract.
    """
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text


# Function to generate a solution based on the extracted text using GPT
def get_solution_from_text(problem_text):
    """
    Generate a solution based on the extracted problem statement using GPT.
    """
    solution = model(problem_text, max_length=300, num_return_sequences=1)
    return solution[0]['generated_text']


# Main function that ties everything together
def main():
    # Capture the screen
    print("Capturing screen...")
    screenshot_path = capture_screen(region=(0, 0, 800, 600))  # Capture a region (you can adjust as needed)

    # Extract text from the captured screenshot
    print("Extracting text from image...")
    extracted_text = extract_text_from_image(screenshot_path)

    print("Extracted Text: \n", extracted_text)

    # Generate solution for the problem statement
    print("Generating solution...")
    solution = get_solution_from_text(extracted_text)

    # Display the solution
    print("\nSolution: \n", solution)


if __name__ == "__main__":
    main()
