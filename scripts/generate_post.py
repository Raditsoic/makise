from langchain_google_genai import ChatGoogleGenerativeAI
from utils import prompt_template, clean_and_parse_response, write_markdown_file
from dotenv import load_dotenv
import random
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=API_KEY)

chain = prompt_template | llm

md_dir = "docs/"

CS_TOPICS = [
    "Data Structures",
    "Algorithms",
    "Object-Oriented Programming",
    "Database Systems",
    "Computer Networks",
    "Operating Systems",
    "Machine Learning",
    "Web Development",
    "Cybersecurity",
    "Software Engineering"
]

if __name__ == "__main__":
    try:
        topic = random.choice(CS_TOPICS)

        raw_response = chain.invoke({"topic": topic})

        response = clean_and_parse_response(raw_response)
        if not response:
            print("Failed to parse and validate response. Exiting.")
            exit(1)
        
        response_data = response.model_dump()

        category_dir = os.path.join(md_dir, topic.replace(" ", "-").lower())

        write_markdown_file(response_data, category_dir) # Write response to markdown file
    except FileNotFoundError as e:
        print(f"File or directory error: {e}")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")