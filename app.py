import pandas as pd
import streamlit as st

# Load dataset
df = pd.read_csv("jobs.csv")

st.set_page_config(page_title="JobYaari Chatbot", layout="centered")
st.title("💼 JobYaari Chatbot")
st.write("Ask me anything about job notifications (Engineering, Science, Commerce, Education).")

# Function to search jobs
def search_jobs(query):
    query = query.lower()
    result = df.copy()

    if "engineering" in query:
        result = result[result["Category"].str.contains("Engineering", case=False, na=False)]
    elif "science" in query:
        result = result[result["Category"].str.contains("Science", case=False, na=False)]
    elif "commerce" in query:
        result = result[result["Category"].str.contains("Commerce", case=False, na=False)]
    elif "education" in query:
        result = result[result["Category"].str.contains("Education", case=False, na=False)]

    # Filter by experience if mentioned
    if "1 year" in query:
        result = result[result["Experience"].str.contains("1 Year", case=False, na=False)]
    if "2 year" in query:
        result = result[result["Experience"].str.contains("2 Years", case=False, na=False)]

    return result

# User input
query = st.text_input("🔍 Your question:")

if query:
    results = search_jobs(query)

    if not results.empty:
        st.success("✅ Here are the jobs I found:")
        st.dataframe(results)
    else:
        st.warning("⚠️ No jobs found matching your query.")



