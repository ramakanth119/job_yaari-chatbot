import pandas as pd
import streamlit as st
#from openai import OpenAI

# Load dataset
df = pd.read_csv("jobs.csv")

# Initialize OpenAI client with your API key
client = OpenAI(api_key="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")  # replace with your real key

st.title("💼 JobYaari AI Chatbot")
st.write("Ask me anything about job notifications (Engineering, Science, Commerce, Education)")

query = st.text_input("Your question:")

if query:
    # Convert dataset to text
    data_text = df.to_string(index=False)

    prompt = f"""
    You are a job assistant for JobYaari.
    Dataset of jobs:
    {data_text}

    Answer the user query strictly using this dataset.
    Query: {query}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a job assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content.strip()
    st.write("### ✅ Answer")
    st.write(answer)

