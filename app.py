import pandas as pd
import re
import streamlit as st

# Load dataset
df = pd.read_csv("jobs.csv")

st.set_page_config(page_title="JobYaari Chatbot", layout="centered")
st.title("💼 JobYaari Chatbot")
st.write("Ask me anything about job notifications (Engineering, Science, Commerce, Education).")

# --- Function to extract salary from string ---
def extract_salary(s):
    if pd.isna(s) or s == "None":
        return 0
    nums = re.findall(r"\d+", str(s))
    return int(nums[0]) * 1000 if "k" in str(s).lower() else (int(nums[0]) if nums else 0)

# --- Main search function ---
def search_jobs(query):
    query = query.lower()
    result = df.copy()

    # --- CATEGORY FILTER ---
    categories = ["engineering", "science", "commerce", "education"]
    for cat in categories:
        if cat in query:
            result = result[result["Category"].str.contains(cat, case=False, na=False)]

    # --- QUALIFICATION FILTER (auto from query) ---
    for qual in result["Qualification"].dropna().unique():
        if str(qual).lower() in query:
            result = result[result["Qualification"].str.contains(qual, case=False, na=False)]

    # --- EXPERIENCE FILTER ---
    exp_match = re.search(r"(\d+)\s*year", query)
    if exp_match:
        years = exp_match.group(1)
        result = result[result["Experience"].astype(str).str.contains(years, na=False)]
    if "fresher" in query or "0 year" in query or "0 experience" in query:
        result = result[result["Experience"].astype(str).str.contains("0", na=False)]

    # --- SALARY FILTER ---
    above_match = re.search(r"(\d+)\s*k?\s*above", query)
    below_match = re.search(r"(\d+)\s*k?\s*below", query)

    result["salary_num"] = result["salary"].apply(extract_salary)

    if above_match:
        value = int(above_match.group(1)) * (1000 if "k" in above_match.group(0) else 1)
        result = result[result["salary_num"] >= value]

    if below_match:
        value = int(below_match.group(1)) * (1000 if "k" in below_match.group(0) else 1)
        result = result[result["salary_num"] <= value]

    return result

# --- User input ---
query = st.text_input("🔍 Your question:")

if query:
    results = search_jobs(query)
    if not results.empty:
        st.success("✅ Here are the jobs I found:")
        st.dataframe(results[['Category','Organization','Vacancies','salary','Age','Experience','Qualification']])
    else:
        st.warning("⚠️ No jobs found matching your query.")
