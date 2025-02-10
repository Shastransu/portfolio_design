# portfolio_design
# Get to Know Me - Interactive Chatbot 🤖  

This is an **AI-powered chatbot** designed to help people learn more about **Shastransu Suprabh**. It allows users to ask questions and receive **intelligent, professional, and conversational responses** based on a database of information.  

## 🌟 Features  
✅ **Ask Me Anything** - The chatbot answers both **casual and professional questions** about Shastransu.  
✅ **Smart AI Responses** - It **retrieves relevant information** and generates meaningful replies.  
✅ **Resume Download** - Users can download Shastransu's **resume** with one click.  
✅ **Social Media Links** - Quick access to **LinkedIn & GitHub profiles**.  
✅ **User-Friendly Interface** - Powered by **Streamlit**, making it easy to use for everyone.  

---

## 🚀 How It Works  
1. **Loads Data** from `data.csv` (contains relevant information).  
2. **Creates AI Embeddings** using OpenAI for better search and retrieval.  
3. **Finds Relevant Information** based on the user's query.  
4. **Generates a Response** using OpenAI's `GPT-4o-mini`.  
5. **Displays the Answer** in an easy-to-read format.  

---

## 🛠️ How to Run Locally  

### **1️⃣ Install Dependencies**  
Make sure you have **Python 3.8+** installed. Then, install required packages:  

```sh
pip install -r requirements.txt
```
-------------------------

# Setting up API Key

I am Open AI API to generate the answer using the 'gpt-4o-mini' model. You can create .env file and paste the API key there
OPEN_AI_API_KEY=<your-api-key-here>

---------------------------
# Running the application
You can run the application using
streamlit run main.py

------------------------------
# 📂 Folder Structure
```
Portfolio_design/
│── main.py                # Main application file
│── data.csv               # Contains relevant data for responses
│── profile.jpg            # Profile picture displayed on UI
│── resume.pdf             # Resume file for download
│── .env                   # Stores API key (DO NOT SHARE)
│── requirements.txt       # Python dependencies
│── README.md              # This file!
```

---------------------------------------

📌 Example Use Cases
🗣️ Casual Greetings:

User: Hi!
Chatbot: Hello! How can I assist you today?

💼 Professional Questions:

User: What are your skills?
Chatbot: My key skills include AI development, cloud computing, and data engineering.

📃 Resume Download:

Click the "Download my Resume" button on the app.

---------------------------------
🔗 Connect with Me
🔹 [Linkedin](https://www.linkedin.com/in/shastransu-suprabh/)
🔹 [GitHub](https://github.com/Shastransu)

---------------------------------------
🏆 Contributing & Feedback
This is a personal chatbot project—feedback and improvements are always welcome!

📩 Feel free to reach out or create a GitHub issue for suggestions.

💙 Thank you for checking out my project! 🚀






