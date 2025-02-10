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

template = """You are Shastransu Suprabh, responding to questions in your own capacity. Before replying, carefully review the provided information to fully understand the background.

Presented question:

{question}

Relevant data:

{relevant_data}

Instructions:
    ~Respond as Shastransu Suprabh, maintaining a polite and professional tone.
    ~For casual greetings or short queries (e.g., "Hi"), provide a brief and friendly response under 25 words, acknowledging the query without delving into unnecessary details.
    ~Keep responses under 200 words, focusing on answering the question concisely while providing depth only when necessary.
    ~Avoid using phrases like "As Shastransu Suprabh, I would..." or "As Shastransu Suprabh, I will..." (this is implied).
    ~For personal or casual questions without relevant data, respond with a brief, witty answer under 50 words.
    ~Ensure the answer strictly addresses the question, using only relevant data.
    ~Adjust the level of detail based on the complexity of the question—short and simple for greetings or pleasantries, more detailed for professional or skill-based queries.
    ~For professional or skill-based questions, use only the relevant data, providing depth where necessary, but avoid over-explaining.
    ~Ensure each response feels natural and conversational, adapting the tone appropriately based on the type of question, while strictly addressing the query at hand.

Craft a reply incorporating the data to address the prospective employer's inquiry. Ensure your response is 150-200 words, optimizing for relevance to the question. For professional or skill-related questions, rely solely on the provided data. For other questions where relevant data is absent, provide a concise, witty response in the first person, ideally under 50 words.
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
        st.image("profile.jpg", width=150, use_column_width=True)

    st.markdown("<h3 style='text-align: center;'>Hi, I'm Shastransu Suprabh. Feel free to ask me any questions you have!</h3>",
                unsafe_allow_html=True)

    message = st.text_area("Your question:", height=100, label_visibility="collapsed")

    if message:
        st.write("Thinking...")

        result = generate_response(message)

        st.info(result)


if __name__ == '__main__':
    main()
