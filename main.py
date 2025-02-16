import streamlit as st
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os
import openai
from openai import RateLimitError
import time

load_dotenv()
api_key = os.environ.get('OPEN_AI_API_KEY')
load_dotenv()

loader = CSVLoader(file_path="data.csv")
documents = loader.load()

# Extract text from Document objects
texts = [doc.page_content for doc in documents]


# Function to handle rate limit errors with exponential backoff
def get_embeddings_with_retry(embedding, texts, max_retries=10, initial_wait=1):
    for retry in range(max_retries):
        try:
            return embedding.embed_documents(texts)
        except RateLimitError as e:
            if retry < max_retries - 1:
                wait_time = initial_wait * (2 ** retry)  # Exponential backoff
                st.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                st.error("Rate limit exceeded. Please check your plan and billing details.")
                return None


# Create embeddings with retry logic
embeddings = OpenAIEmbeddings()
embedding_vectors = get_embeddings_with_retry(embeddings, texts)

db = FAISS.from_documents(documents, embeddings)


def retrieve_info(query):
    similar_response = db.similarity_search(query, k=4)
    page_contents_array = [doc.page_content for doc in similar_response]
    return "\n\n".join(page_contents_array)


llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

template = """You are Shastransu Suprabh

- Respond naturally as if you are having a direct conversation.
- Your tone should be friendly, conversational, and authentic, as if you're chatting directly with someone.

#### Question received:
{question}

#### Context about yourself:
{relevant_data}

#### Personality Guidelines for Shastransu Suprabh

1. **Natural First-Person Voice**
- Speak naturally as Shastransu Suprabh using "I" and "me"
- Keep responses conversational and authentic
- Example: "Hi there! I'm Shastransu Suprabh - great to meet you!"

2. **Knowledge Boundaries**
- Only use information from provided context
- For unknown topics, be honest and friendly:
  "That's an interesting question! While I'm not familiar with that specific topic, I'd love to learn more about it."

3. **Personal Questions**
- For questions outside context, redirect gracefully:
  "I prefer to focus on [relevant topic], but I'd love to hear your thoughts on it!"

4. **Self-Introduction**
- Naturally incorporate context-based details
- Keep it warm and genuine
- Example: "Hey! I'm Shastransu, currently doing my Master's in Applied Machine Intelligence at Northeastern."

5. **Technical Communication**
- Keep responses under 150 words
- Focus on clarity and accessibility
- Show genuine enthusiasm for the subject matter

6. **Core Principles**
- Stay authentic and conversational
- Maintain friendly professionalism
- Be direct and clear in all responses

#### Formatting and Response Guidelines

## Markdown Structure
1. **Organization Tools**
   - Use bullet points for related items
   - Apply numbered lists for sequential steps

2. **Text Emphasis**
   - **Bold** for key concepts
   - _Italic_ for subtle emphasis
   - `Code formatting` for technical terms

3. **Visual Hierarchy**
   - Use headers (H1-H4) for clear sections
   - Keep spacing consistent
   - Group related information
   - Add line breaks for readability

### Template Structure
[Greeting]
- Start with a warm, context-appropriate hello
- Example: "Hi there!" or "Hello, thanks for asking!"

[Main Response]
- Provide direct, clear answer
- Include relevant personal experience
- Keep tone conversational

[Supporting Details]
- Add specific examples when relevant
- Share context-appropriate details
- Maintain authenticity

[Engagement/Closure]
- End with an engaging element
- Ask a relevant follow-up question
- Or provide a natural conclusion

---
### Example Prompt Pattern in Action:
**Context about yourself:** "I'm pursuing my Master's in Applied Machine Intelligence at Northeastern, based in Boston."  
**Question received:** "What made you choose Applied Machine Intelligence?"  
**Response:**  
"I was drawn to the practical applications of AI! After seeing how machine learning is revolutionizing industries, I knew I wanted to dive deeper. Northeastern's hands-on approach really appealed to me."

"""

prompt = PromptTemplate(
    input_variables=["question", "relevant_data"],
    template=template
)

chain = (
        {"question": RunnablePassthrough(), "relevant_data": lambda x: retrieve_info(x["question"])}
        | prompt
        | llm
)


def generate_response(question):
    response = chain.invoke({"question": question})
    return response.content


def main():
    st.set_page_config(
        page_title="Get to know me", page_icon=":male-technologist:")

    st.markdown("""
        <style>
        /* Clean dark theme background */
        .stApp {
            background: #1a1a1a;
        }

        /* Minimal styling for content */
        .stMarkdown {
            color: #ffffff;
        }

        /* Social icons styling - keeping the hover effects */
        .social-icons {
            text-align: right;
            padding: 10px 0;
        }
        .social-icons a {
            display: inline-block;
            margin-right: 10px;
        }
        .social-icons a:last-child {
            margin-right: 0;
        }
        .social-icons a img {
            width: 30px;
            transition: all 0.3s ease;
            filter: brightness(0.9);
        }
        .social-icons a img:hover {
            transform: translateY(-3px) scale(1.1);
            filter: brightness(1);
        }

        /* Clean text styling */
        h1, h3 {
            color: #ffffff !important;
            font-weight: 600;
        }
        p {
            color: #e0e0e0 !important;
        }

        /* Subtle button styling */
        .stDownloadButton button {
            background-color: #333333 !important;
            color: white !important;
            border-radius: 5px;
            border: none !important;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        .stDownloadButton button:hover {
            background-color: #444444 !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }

        /* Clean text area styling */
        .stTextArea textarea {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 5px;
            padding: 10px;
        }
        .stTextArea textarea:focus {
            box-shadow: 0 0 0 2px rgba(77, 77, 77, 0.2);
        }

        /* Minimal response container */
        .response-container {
            background-color: #2d2d2d;
            color: #ffffff;
            padding: 1.5rem;
            border-radius: 5px;
            margin-top: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)

    # Move resume download and social icons to the top
    col4, col5 = st.columns([3, 1])
    with col4:
        with open("resume.pdf", "rb") as file:
            st.download_button(label="Download my Resume", data=file, file_name="resume.pdf",
                               mime="application/pdf")
    with col5:
        st.markdown("""
               <div style='text-align: right;'>
                   <a href='https://www.linkedin.com/in/shastransu-suprabh/' target='_blank' style='margin-right: 10px;'>
                       <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' width='30'/>
                   </a>
                   <a href='https://github.com/Shastransu' target='_blank'>
                       <img src='https://cdn-icons-png.flaticon.com/512/733/733553.png' width='30'/>
                   </a>
               </div>
           """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>Get to know me</h1>", unsafe_allow_html=True)

    # Smaller profile picture
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("profile.jpg", width=150, use_container_width=True)

    st.markdown("<h3 style='text-align: center;'>Hi, I'm Shastransu Suprabh. Feel free to ask me any questions you have!</h3>",
                unsafe_allow_html=True)

    # Add a hint before the text area
    st.markdown("""
            <div style='
                color: #888888;
                font-size: 0.8em;
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                gap: 5px;
            '>
                <span>💡</span>
                <span>Press Ctrl+Enter to submit your question</span>
            </div>
        """, unsafe_allow_html=True)
    # Text area for input
    message = st.text_area(
        "Your question:",
        height=120,
        label_visibility="collapsed",
        message=st.text_area("Your question:", height=100, label_visibility="collapsed"),
        placeholder = "Type your question here...",
        key = "question_input"
    )
    if message:
        if message:
            with st.spinner("Thinking... Please wait"):
                st.write("Thinking...")
            result = generate_response(message)
    result = generate_response(message)

    st.markdown(f"""
                <div class='response-container'>
                    {result}
            st.info(result)
                </div>
            """, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
