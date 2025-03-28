from langchain_community.document_loaders import YoutubeLoader
from langchain_community.llms import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()

def create_vector_db_from_youtube(video_url:str) -> FAISS:
    loader = YoutubeLoader.from_youtube_url(video_url)
    transcript = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chuck_size=1000,chunk_overlap=100)
    docs=text_splitter.split_documents(transcript)

    db=FAISS.from_documents(docs,embeddings)
    return db