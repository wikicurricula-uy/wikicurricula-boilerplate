'''
This script makes a call to the wikidata API by taking in the language_code, e.g "en" as an argument.
The result(data) of this query is then processed to get the artcle name, id and material of the articles into "article_name.csv" and "subjects.csv" files. 
The two(2) csv files produced canbe further used for analysis by the bot.py and for visualization.
'''


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

# make a request to wikidata API to fetch Ghana's curriculum by passing the language code as an argument
def fetch_data(language_code):
    sparql_query = f"""
    SELECT DISTINCT (STRAFTER(STR(?item), "http://www.wikidata.org/entity/") AS ?qid) ?item ?itemLabel ?articleName ?programLabel
    WHERE {{
        ?substrand wdt:P31 wd:Q600134.
        ?substrand wdt:P921 ?item.
        ?substrand wdt:P17 wd:Q117. #Uruguay

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

    # Set up parameters for the HTTP request
    params = {
        "query": sparql_query,
        "format": "json",
    }

    # HTTP request to the Wikidata endpoint
    response = requests.get(wikidata_endpoint, headers=headers, params=params) # HTTP request to the Wikidata endpoint

    # Check if the request was successful i.e it has status code 200
    if response.status_code == 200:
        data = response.json()

        # Extract and print the results
        results = data.get("results", {}).get("bindings", [])
        return results

    else:
        print(f"Error: Unable to fetch data. Status Code: {response.status_code}")


# save article name in article_name.csv
def get_articles(results):
    # Open the file in write mode to clear its contents
    with open("article_name.csv", "w") as file:
        pass  # This line clears the content of the file

    # Open the file in append mode and write data for each result
    with open("article_name.csv", "a") as file:
        for result in results:
            article_name = result.get("articleName", {}).get("value", "")
            if article_name != "":
                file.write(f"{article_name}\n")


# save subject and id of articles in subjects.csv
def get_id_and_subjects(results):
    with open("subjects.csv", "w") as file:
        pass  # This line clears the content of the file
        fields = ["id_wikidata", "material"]
        writer = csv.DictWriter(file, fieldnames=fields, lineterminator='\n')

        writer.writeheader()

        for result in results:
            id_wikidata = result.get("qid", {}).get("value", "")
            material = result.get("programLabel", {}).get("value", "")
            # material = result.get("programLabel", {}).get("value", "")
            if "Curriculum" in material:
                material = material.split("Curriculum")[0]

                        
            if "Science" in material:
                material = "Science"
            
            writer.writerow({"id_wikidata": id_wikidata, "material": material})

if __name__ == "__main__":
    query_result = fetch_data(language_code)
    get_articles(query_result)
    get_id_and_subjects(query_result)
    