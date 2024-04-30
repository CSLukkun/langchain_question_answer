import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import SimpleJsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import os
import pyperclip

st.title('🦜🔗 Quickstart App')
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

if openai_api_key:
    planner = (
        ChatPromptTemplate.from_messages(
            [
                ("human", "{question}")
            ]) 
        | ChatOpenAI(
            openai_api_key = openai_api_key
        )
        | StrOutputParser()
        | {"base_response": RunnablePassthrough()}
    )

    question_and_answer_generate = (
        ChatPromptTemplate.from_template(
        """Please generate pairs of question and answers based on {base_response}. The returned format like this:
        
        
        1.What is the None type in Python? == The None type in Python is represented by the keyword 'None' and is used to define a null value or absence of a value.
        """
        )
        | ChatOpenAI(
            openai_api_key = openai_api_key
        )
        | StrOutputParser()
    )

    chain = (
        planner | question_and_answer_generate
    )

    def generate_response(input_text):
        res = chain.invoke({
            "question": input_text
        })
        st.info(res)
        return res

    res = None  # Initialize res outside the with block

    with st.form("my_form"):
        if os.environ["OPENAI_API_KEY"]:
            openai_api_key = os.environ["OPENAI_API_KEY"]
        text = st.text_area('Enter text:', 'what is a tuple in python')
        submitted = st.form_submit_button('Submit')
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!')
        if submitted and openai_api_key.startswith('sk-'):
            res = generate_response(text)