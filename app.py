import pandas as pd
import streamlit as st
import re

# Load dataset
df = pd.read_csv("jobs.csv")

st.set_page_config(page_title="JobYaari Chatbot", layout="centered")
st.title("💼 JobYaari Chatbot")
st.write("Ask me anything about job notifications (Engineering, Science, Commerce, Education).")

# Function to search jobs
def search_jobs(query):
    query = query.lower()
    result = df.copy()

    # -------- Category filter --------
    if "engineering" in query:
        result = result[result["Category"].str.contains("Engineering", case=False, na=False)]
    elif "science" in query:
        result = result[result["Category"].str.contains("Science", case=False, na=False)]
    elif "commerce" in query:
        result = result[result["Category"].str.contains("Commerce", case=False, na=False)]
    elif "education" in query:
        result = result[result["Category"].str.contains("Education", case=False, na=False)]

    # -------- Experience filter --------
    if "fresher" in query or "freshers" in query:
        result = result[result["Experience"].str.contains("Fresher", case=False, na=False)]
    else:
        # Look for "X year(s)" pattern
        match = re.search(r"(\d+)\s*year", query)
        if match:
            years = match.group(1)
            result = result[result["Experience"].str.contains(years, case=False, na=False)]

    # -------- Salary filter --------
    # Normalize salary column (assume numeric or strings like "20000", "30k", "40,000")
    if "Salary" in result.columns:
        # Convert to numeric
        result["Salary_num"] = (
            result["Salary"]
            .astype(str)
            .str.replace(r"[^\d]", "", regex=True)  # keep only numbers
            .replace("", "0")
            .astype(int)
        )

        # Example: "20k above" or "20000 above"
        match_above = re.search(r"(\d+)\s*k?\s*above", query)
        if match_above:
            value = int(match_above.group(1)) * (1000 if "k" in query else 1)
            result = result[result["Salary_num"] >= value]

        # Example: "50000 below"
        match_below = re.search(r"(\d+)\s*k?\s*below", query)
        if match_below:
            value = int(match_below.group(1)) * (1000 if "k" in query else 1)
            result = result[result["Salary_num"] <= value]

    return result

# User input
query = st.text_input("🔍 Your question:")

if query:
    results = search_jobs(query)

    if not results.empty:
        st.success("✅ Here are the jobs I found:")
        st.dataframe(results.drop(columns=["Salary_num"], errors="ignore"))
    else:
        st.warning("⚠️ No jobs found matching your query.")
