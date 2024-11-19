# **Web Scraping Chatbot with Hugging Face Question-Answering API**

This project demonstrates a simple chatbot that can scrape content from a website, process it, and answer user questions using the Hugging Face Inference API.


## **Features**
- Scrapes and cleans website content for context.
- Uses a Hugging Face model (`roberta-base-squad2`) for question answering.
- Caches website content locally to optimize performance.
- Provides an interactive chatbot interface for user queries.



## **Installation**

### **Requirements**
- Python 3.8 or higher
- Dependencies listed in `requirements.txt`

### **Setup**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/web-scraping-chatbot.git
   cd web-scraping-chatbot
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the API key:
   - Create a file named `api.env` in the project root.
   - Add the following line, replacing `your_api_key` with your Hugging Face API key:
     ```plaintext
     API_KEY=your_api_key
     ```
