import streamlit as st
from agents.summary_agent import summarize_competitor_update


st.set_page_config(page_title="Competitor Tracker AI", layout="centered")
st.title("🕵️‍♀️ Competitor Feature Tracker for PMs")

st.markdown("""
Enter URLs of competitor changelogs, websites, or blog posts. Our AI agent will extract and summarize important updates like:
- UI Changes
- Product Launches
- Pricing Changes

Built with GPT, LangChain, and Streamlit 🚀
""")

urls_input = st.text_area("Paste 2-3 Competitor URLs (one per line):", height=150)

if st.button("Analyze Changes"):
    if not urls_input.strip():
        st.warning("Please enter at least one URL.")
    else:
        with st.spinner("🔍 Analyzing competitor updates..."):
            urls = [url.strip() for url in urls_input.strip().split("\n") if url.strip()]
            summaries = summarize_competitor_update(urls)

        st.success("Analysis Complete!")
        for url, summary in summaries.items():
            st.subheader(f"🔗 {url}")
            st.markdown(summary)
