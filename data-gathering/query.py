import requests
import csv
import json
import sys  #Import the sys module to access command-line arguments

# Check if the language code is provided as a command-line argument
if len(sys.argv) < 2:
    print("Please provide the language code as a command-line argument (e.g., 'en' for English).")
    sys.exit(1)

# Get the language code from the command-line argument
language_code = sys.argv[1]

# Define your SPARQL query
sparql_query = f"""
SELECT DISTINCT (STRAFTER(STR(?item), "http://www.wikidata.org/entity/") AS ?qid) ?item ?itemLabel ?articleName ?programLabel
WHERE {{
  ?substrand wdt:P31 wd:Q600134.
  ?substrand wdt:P921 ?item.
  ?substrand wdt:P17 wd:Q77. #Uruguay
  
  OPTIONAL {{ ?substrand wdt:P361 ?program. }}
  OPTIONAL {{ ?articulo schema:about ?item;
    schema:isPartOf <https://{language_code}.wikipedia.org/>. 
    ?articulo schema:name ?articleName.
  }}
  
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{language_code}". }}
}}
"""

# Define the Wikidata Query Service endpoint URL
wikidata_endpoint = "https://query.wikidata.org/sparql"

# Define headers for the HTTP request
headers = {
    "User-Agent": "Python SPARQL Client",
    "Accept": "application/sparql-results+json",
}

# Define the query parameters
params = {
    "query": sparql_query,
    "format": "json",
}

try:
    # Send a GET request to the Wikidata Query Service endpoint
    response = requests.get(wikidata_endpoint, headers=headers, params=params)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        data = json.loads(response.text)

        # Check if there are results in the response
        if "results" in data:
            # Extract and save the results to a CSV file
            with open("query_result.csv", mode="w", newline="", encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)

                # Write header row
                csv_writer.writerow(["qid", "item", "itemLabel", "articleName", "programLabel"])

                # Write data rows
                for item in data["results"]["bindings"]:
                    qid = item.get("qid", {}).get("value", "")  # Handle missing qid
                    item_uri = item.get("item", {}).get("value", "")
                    item_label = item.get("itemLabel", {}).get("value", "")
                    article_name = item.get("articleName", {}).get("value", "")
                    program_label = item.get("programLabel", {}).get("value", "")
                    csv_writer.writerow([qid, item_uri, item_label, article_name, program_label])

            print("Results saved to query_result.csv")
        else:
            print("No results found for the query.")

    else:
        print(f"Request failed with status code {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {str(e)}")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
