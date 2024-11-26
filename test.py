from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

print(genai)

def translate(text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Explain how AI works")
    return response.text

if __name__ == '__main__':
    response = translate("Hello!")
    print(f"2. This is the response in main: {response}")
