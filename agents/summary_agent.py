import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv

# ✅ Load Gemini API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Define Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# ✅ Function to extract raw website text
def fetch_website_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=' ', strip=True)
        return text[:1200]  # Gemini input limit
    except Exception as e:
        return f"Error fetching {url}: {str(e)}"

# ✅ Function to summarize using Gemini
def summarize_with_gemini(text, url):
    try:
        prompt = f"""
You are an AI Product Analyst. Analyze the following content from a competitor's product page and extract:
- Any product updates or new feature releases
- Any UI or UX changes
- Any changes in pricing, plans, or subscriptions
- Anything useful for a product manager to know

Source: {url}

Content:
{text}

Summarize these insights clearly:
"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error summarizing {url}: {str(e)}"

# ✅ Main function to summarize list of URLs
def summarize_competitor_update(urls):
    summaries = {}
    for url in urls:
        print(f"🔄 Fetching content from {url}")
        raw_text = fetch_website_text(url)
        if raw_text.startswith("Error"):
            summaries[url] = raw_text
        else:
            print(f"✍️ Summarizing {url}")
            summary = summarize_with_gemini(raw_text, url)
            summaries[url] = summary
    return summaries

# ✅ Run this script
# if __name__ == "__main__":
#     urls = [
#         "https://www.notion.so/whats-new",
#         "https://pitch.com/changelog"
#     ]

#     summaries = summarize_competitor_update(urls)

#     print("\n📌 Final Summaries:\n")
#     for url, summary in summaries.items():
#         print(f"🔗 {url}\n{summary}\n{'='*80}")
if __name__ == "__main__":
    urls = [
        "https://www.notion.so/whats-new",
        "https://pitch.com/changelog"
    ]

    summaries = summarize_competitor_update(urls)

    for url, summary in summaries.items():
        print(f"\n🔗 {url}\n{summary}\n{'='*80}")
