from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

# Configure GenAI Key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Function to load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    # Combine the prompt and question into a single string
    combined_prompt = prompt + question
    response = model.generate_content(combined_prompt)
    return response.text

# Function to retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Define your prompt as a string
prompt = """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION. 

    For example:
    - Example 1: How many entries of records are present? 
      SQL command: SELECT COUNT(*) FROM STUDENT;

    - Example 2: Tell me all the students studying in Data Science class? 
      SQL command: SELECT * FROM STUDENT WHERE CLASS="Data Science";

    The SQL code should not have ``` in the beginning or end, and the SQL word should not appear in the output.
"""

# Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")

submit = st.button("Submit")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print(response)
    sql_result = read_sql_query(response, "student.db")
    st.subheader("The Response is")
    for row in sql_result:
        print(row)
        st.header(row)
