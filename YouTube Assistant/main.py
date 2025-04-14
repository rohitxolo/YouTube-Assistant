import streamlit as st
import langchain_helper as lch
import textwrap

import langchain_helper as lch  # Import your helper functions

# Example YouTube URL (replace with a valid URL)
youtube_url = "https://www.youtube.com/watch?v=lG7Uxts9SXs"

# Create the vector database from the YouTube video
db = lch.create_vector_db_from_youtube(youtube_url)

# Query the vector database
query = "What is the main topic of the video?"  # Your example query
response = lch.get_response_from_query(db, query)

# Output the response
print(response)


st.title("YouTube Assistant")

with st.sidebar:
    with st.form(key="my_form"):
        youtube_url = st.sidebar.text_area(
            label="Enter YouTube Video URL",
            max_chars=100
        )
        query = st.sidebar.text_area(
            label="Enter your question about Video",
            max_chars=100,
            key = "query"
        )

        submit_button = st.form_submit_button(label="Submit")

if query and youtube_url:
    db = lch.create_vector_db_from_youtube(youtube_url)
    response = lch.get_response_from_query(db, query)
    st.subheader("Answer:")
    st.text(textwrap.fill(response, width=100))
