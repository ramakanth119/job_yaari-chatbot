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
    if "fresher" in query or "freshers" in query or "0 experience" in query or "zero experience" in query:
        result = result[result["Experience"].str.contains("0|Fresher", case=False, na=False)]
    else:
        # Look for numbers in query (1, 2, 3, 5 etc.)
        match = re.search(r"(\d+)", query)
        if match:
            years = match.group(1)
            result = result[result["Experience"].str.contains(years, case=False, na=False)]

    # -------- Salary filter --------
    if "salary" in df.columns or "Salary" in df.columns or "salary" in result.columns:
        # Detect column name properly
        salary_col = None
        for col in result.columns:
            if col.lower() == "salary":
                salary_col = col
                break

        if salary_col:
            # Convert salary to numbers
            result["Salary_num"] = (
                result[salary_col]
                .astype(str)
                .str.replace(r"[^\d]", "", regex=True)  # keep only digits
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
        # Drop helper column before showing
        st.dataframe(results.drop(columns=["Salary_num"], errors="ignore"))
    else:
        st.warning("⚠️ No jobs found matching your query.")
