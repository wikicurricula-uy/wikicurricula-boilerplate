import csv
import requests


# make a request to wikidata API to fetch Ghana's curriculum
def fetch_wikidata_info():
    # Wikidata endpoint URL for the SPARQL query
    wikidata_endpoint = "https://query.wikidata.org/sparql"

    # SPARQL query to get information about Ghana's national curriculum
    sparql_query = """
    SELECT DISTINCT (STRAFTER(STR(?item), "http://www.wikidata.org/entity/") AS ?qid) ?item ?itemLabel ?nombreDelArticulo ?programaLabel
    WHERE {
        ?substrand wdt:P31 wd:Q600134.
        ?substrand wdt:P921 ?item.
        ?substrand wdt:P17 wd:Q77. #Uruguay
  
        OPTIONAL { ?substrand wdt:P361 ?programa. }
        OPTIONAL { ?articulo schema:about ?item;
        schema:isPartOf <https://es.wikipedia.org/>. 
        ?articulo schema:name ?nombreDelArticulo.
  }
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "es". }
 
}
    """

    # Set up headers for the HTTP request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Set up parameters for the HTTP request
    params = {
        "query": sparql_query,
        "format": "json",
    }

    # Make the HTTP request to the Wikidata endpoint
    response = requests.get(wikidata_endpoint, headers=headers, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract and print the results
        results = data.get("results", {}).get("bindings", [])
        return results

    else:
        print(f"Error: Unable to fetch data. Status Code: {response.status_code}")


# store article name in query.csv
def store_articles(results):
   
    # delete the contents of the file before starting
     query = open('query.csv',"w")
   
   # Truncate the "results.txt" file to remove existing content
     query.truncate(0)
   
     query.close()

     with open("query.csv","a") as file:
        for result in results:
            article_name = result.get("nombreDelArticulo", {}).get("value", "")
            if article_name != "":
              file.write(f"{article_name}\n")

# store subject and id in subjects.csv
def store_subjects(results):

    # delete the contents of the file before starting
    results = open('subjects.csv',"w")
   
   # Truncate the "results.txt" file to remove existing content
    results.truncate(0)
    results.close()

    # Open the file outside the loop to write the header only once
    with open("subjects.csv", "a", newline='') as file:
        fieldnames = ["id_wikidata", "material"]
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator='\n')

        # Write the header outside the loop
        writer.writeheader()

        for result in results:
            id_wikidata = result.get("qid", {}).get("value", "")
            material, _ = result.get("programaLabel", {}).get("value", "").split("Curriculum")
            
            if "Science" in material:
                material = "Science"
            # Write the row for each result
            writer.writerow({"id_wikidata": id_wikidata, "material": material})

if __name__ == "__main__":
    query_results = fetch_wikidata_info()
    store_articles(query_results)
    store_subjects(query_results)
