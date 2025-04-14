from langchain_community.document_loaders import YoutubeLoader
from langchain_community.llms import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()
#print(load_dotenv())

embeddings = OpenAIEmbeddings()

def create_vector_db_from_youtube(video_url:str) -> FAISS:
    loader = YoutubeLoader.from_youtube_url(video_url)
    transcript = loader.load()

    transcript_text = " ".join([t.text.strip() for t in transcript])  # Assuming `text` is the correct attribute


    text_splitter = RecursiveCharacterTextSplitter(chuck_size=1000,chunk_overlap=100)
    docs=text_splitter.split_documents(transcript)

    db=FAISS.from_documents(docs,embeddings)
    return db

def get_response_from_query(db,query,k=4):
    #text-davinci can handle 4079 tokens
    docs = db.similarity_search(query,k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    llm = openai.OpenAI(model="text-davinci-003")
    promt = PromptTemplate(
        input_variables=["question", "docs"],
        template="""You are a helpful youtube assistant that can answer questions about
         videos based on videos transcript.

         Answer the following question:{question}
         By searching the following transcript:{docs}

         only use the factual information from the transcript to answer the question.

         if you feel like you don't have enough information to answer the question, say "I don't know".
         Be concise and clear in your answer.
         """
    )
    chain = LLMChain(llm=llm, prompt=promt)
    response = chain.run(question=query, docs=docs_page_content)
    response = response.replace("\n"," ")
    return response
    
