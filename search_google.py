import pandas as pd
import requests
import time
from datetime import datetime
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
MAX_SEARCHES = int(os.getenv("MAX_SEARCHES", 10))

if not API_KEY or not SEARCH_ENGINE_ID:
    print("[ERROR] Missing API key or Search Engine ID in .env file.")
    sys.exit(1)

def search_google(query, max_results=MAX_SEARCHES):
    """Query Google Custom Search and return results"""

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": max_results
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("items", [])
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed query '{query}': {e}")
        return []

def main():
    input_file = "queries.csv"
    timestamp = datetime.now().isoformat().replace(":", "-").split(".")[0]  # e.g. '2025-08-04T14-30-00'
    output_file = f"search_results_{timestamp}.csv"

    # Read input queries
    try:
        queries_df = pd.read_csv(input_file)
    except Exception as e:
        print(f"[ERROR] Could not read {input_file}: {e}")
        sys.exit(1)

    if queries_df.empty or queries_df.shape[1] == 0:
        print("[ERROR] No query column found in input.")
        sys.exit(1)

    query_col = queries_df.columns[0]  # Assume first column has queries
    results = []

    # Search each query
    for query in queries_df[query_col].dropna().unique():
        print(f"    Searching: {query}")
        items = search_google(query)
        for i, item in enumerate(items, 1):
            results.append({
                "query": query,
                "result_rank": i,
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", ""),
                "display_link": item.get("displayLink", ""),
                "formatted_url": item.get("formattedUrl", ""),
                "search_timestamp": datetime.now().isoformat()
            })
        time.sleep(1)  # Avoid rate-limiting

    # Save results to csv output file
    if results:
        output_df = pd.DataFrame(results)
        output_df.to_csv(output_file, index=False)
        print(f"Finished: {len(results)} results written to '{output_file}'")
    else:
        print("Error: No results returned.")

if __name__ == "__main__":
    main()
