import streamlit as st

from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

from youtube_transcript_api import YouTubeTranscriptApi

from streamlit import session_state as ss

st.title('Youtube Video Summarizer')

# Load the model
if 'llm' not in ss:
    with st.spinner("Loading Model"):
        ss.llm = Ollama(model = 'llama3.1')

def get_video_id(link):
    ind = link.rindex('=')
    return link[ind+1:]

def get_transcript(id):
    transcript_data = YouTubeTranscriptApi.get_transcript(id)

    content = ""

    for data in transcript_data:
        content += data['text'] + " "
    
    return content

def get_response(content):

    prompt_template = """
You are provided with a transcript of a youtube video by the user.
Provide the user with a detailed summary of the transcript.

### Transcript:
{transcript}
"""

    final_prompt = PromptTemplate.from_template(template = prompt_template,kwargs={'input_variable':['transcript']})

    return ss.llm.invoke(final_prompt.format(transcript = content))

video_link = st.text_input('Enter the youtube video link')

submit = st.button('Submit')

if submit:
    with st.spinner('Generating Summary'):
        video_id = get_video_id(video_link)

        transcript = get_transcript(video_id)

        response = get_response(transcript)

    st.video(video_link)
    st.subheader('Summary',divider=True)
    st.write(response)

