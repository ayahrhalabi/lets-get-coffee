import os
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from google.oauth2 import service_account
from dotenv import load_dotenv
import numpy as np

load_dotenv()

# ==== Define a Patched Embedding class to flatten embeddings ====
class PatchedGoogleEmbeddings(GoogleGenerativeAIEmbeddings):
    def embed_query(self, text, **kwargs):
        output = super().embed_query(text, **kwargs)
        while isinstance(output[0], list):
            output = output[0]
        return output

    def embed_documents(self, texts, **kwargs):
        outputs = super().embed_documents(texts, **kwargs)
        def flatten(x):
            while isinstance(x[0], list):
                x = x[0]
            return x
        return [flatten(e) for e in outputs]

# Pooling

class PooledGoogleEmbeddings(GoogleGenerativeAIEmbeddings):
    def embed_query(self, text, **kwargs):
        output = super().embed_query(text, **kwargs)
        return output

    def embed_documents(self, texts, **kwargs):
        outputs = super().embed_documents(texts, **kwargs)
        return outputs[0]
    
    
# ==== Load Models ====
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

DATA_PATH = "updated_coffee_shops.csv"
DB_DIR    = "./chroma_db"

embedding_model = PooledGoogleEmbeddings(model="models/embedding-001")

llm_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.75, top_p=0.8)

# ==== Load or create the vectorstore ====
if not os.path.isdir(DB_DIR) or not os.listdir(DB_DIR):
    df = pd.read_csv(DATA_PATH)
    loader = DataFrameLoader(df, page_content_column="Combined Review Text")
    docs = loader.load()

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding_function=embedding_model,
        persist_directory=DB_DIR
    )
    vectorstore.persist()
else:
    vectorstore = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embedding_model
    )

retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

# ==== Define Prompt ====
rag_prompt = PromptTemplate.from_template("""You're a friendly and knowledgeable coffee shop expert in Los Angeles.
Recommend a coffee shop to the user who asked: "{user_query}"

{context}

Provide your recommendation in a conversational way, explaining why this coffee shop would be perfect for them.
Include specific details about the coffee shop's features, atmosphere, and what makes it unique.
Make sure to prominently include the name and address in your response.""")

# ==== Main answering function ====
def answer_question(user_query: str) -> str:
    docs = retriever.invoke(user_query)

    context = "\n\n".join([
        f"Coffee Shop: {doc.metadata.get('Name', 'Unknown')}\n"
        f"Address: {doc.metadata.get('Address', 'N/A')}\n"
        f"Detail URL: {doc.metadata.get('Website', 'N/A')}\n"
        f"Description: {doc.page_content}"
        for doc in docs[:3]
    ])

    prompt = rag_prompt.format(context=context, user_query=user_query)
    response = llm_model.invoke(prompt)
    return response.content

# ==== Test call ====
#if __name__ == "__main__":
    print(answer_question("What is the best matcha in LA?"))

