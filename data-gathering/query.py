import csv
import sys
from SPARQLWrapper import SPARQLWrapper,JSON


# make a request to wikidata API to fetch Ghana's curriculum
def fetch_wikidata_info(language,code):
      # Wikidata endpoint URL for the SPARQL query
    wikidata_endpoint = "https://query.wikidata.org/sparql"

    # SPARQL query to get information about Ghana's national curriculum
    sparql_query = f"""
    SELECT DISTINCT (STRAFTER(STR(?item), "http://www.wikidata.org/entity/") AS ?qid) ?item ?itemLabel ?nombreDelArticulo ?programaLabel
    WHERE {{
      ?substrand wdt:P31 wd:Q600134.
      ?substrand wdt:P921 ?item.
      ?substrand wdt:P17 wd:Q{code}.

      OPTIONAL {{ ?substrand wdt:P361 ?programa. }}
      OPTIONAL {{ ?articulo schema:about ?item;
        schema:isPartOf <https://{language}.wikipedia.org/>. 
        ?articulo schema:name ?nombreDelArticulo.
      }}

      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{language}". }}
    }}
    """
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0],sys.version_info[1])

    sparql = SPARQLWrapper(wikidata_endpoint, agent=user_agent)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def store_articles(results):
    # Extract article names from results
    article_names = [result.get("nombreDelArticulo", {}).get("value", "") for result in results['results']['bindings']]

    # Remove empty names
    article_names = [name for name in article_names if name]

    # Sort article names alphabetically
    article_names.sort()

    # Write sorted article names to the file
    with open("query.csv", "w", encoding="utf-8", errors="replace") as file:
        for article_name in article_names:
            file.write(f"{article_name}\n")


# store subject and id in subjects.csv
#def store_subjects(results):
    # Open the file outside the loop to write the header only once
    #with open("subjects.csv", "a", newline='') as file:
        #fieldnames = ["id_wikidata", "material"]
        #writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator='\n')

        # Write the header outside the loop
        #writer.writeheader()

        #for result in results:
            #id_wikidata = result.get("qid", {}).get("value", "")
            #material, _ = result.get("programaLabel", {}).get("value", "").split("Curriculum")
            
            #if "Science" in material:
                #material = "Science"
            # Write the row for each result
            #writer.writerow({"id_wikidata": id_wikidata, "material": material})33

if __name__ == "__main__":
    query_results = fetch_wikidata_info()
    store_articles(query_results)
    #store_subjects(query_results)

