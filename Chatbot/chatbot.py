
import requests
import os
import _pickle
import re
import time
from bs4 import BeautifulSoup
from gensim.parsing.preprocessing import remove_stopwords
from dotenv import load_dotenv


load_dotenv("api.env") 

API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"


headers = {"Authorization": f"Bearer {os.getenv('API_KEY')}"}
print(f"API_KEY loaded: {os.getenv('API_KEY')}")


def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        website_content = remove_stopwords(soup.get_text())
        cleaned_content = clean_webpage_content(website_content)
        return cleaned_content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None

def clean_webpage_content(content):
    
    content = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<[^>]+>', '', content)
    content = ' '.join(content.split())
    return content

def load_context(url):
    try:
        with open("data.pkl", "rb") as f:
            loaded_data = _pickle.load(f)
            context = loaded_data.get("context", "")
        
    except FileNotFoundError:
        
        context = scrape_website(url)
        if not context:
            print("Failed to scrape content.")
            return None
        data = {"label": "BotPenguin", "context": context}
        with open("data.pkl", "wb") as file:
            _pickle.dump(data, file)
        
    return context

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error with the API request: {e}")
        print(f"Response: {e.response.text}")  
        return {"answer": "Error querying the model."}

def answer_question(question, context):
    if not context:
        print("No context available to answer the question.")
        return "No context available."
    
    payload = {"inputs": {"question": question, "context": context}}
    try:
        response = query(payload)
        if 'estimated_time' in response:
            print(f"Model loading, please wait for {response['estimated_time']} seconds...")
            time.sleep(response['estimated_time'])
            response = query(payload)
        answer = response.get("answer", "Sorry, I couldn't find an answer.")
        return answer
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "Error generating answer."

def run_chatbot(url):
    context = load_context(url)

    if not context:
        print("Could not load context. Exiting chatbot.")
        return

    print("Chatbot is ready! Ask a question or type 'exit' to end.")
    while True:
        question = input("You: ")
        if question.lower() == 'exit':
            print("Chatbot session ended.")
            break
        answer = answer_question(question, context)
        print(f"Chatbot: {answer}\n")



if __name__ == "__main__":
    website_url = "https://botpenguin.com/"  
    run_chatbot(website_url)
