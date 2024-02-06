import json
import csv
import sys
from SPARQLWrapper import SPARQLWrapper, JSON

# Load configuration from JSON file
with open("file_config.json", "r") as config_file:
    CONFIG = json.load(config_file)

# SPARQL query template
SPARQL_QUERY = """
SELECT DISTINCT (STRAFTER(STR(?item), "http://www.wikidata.org/entity/") AS ?qid) ?item ?itemLabel ?nombreDelArticulo ?programaLabel
WHERE {{
  ?substrand wdt:P31 wd:Q600134.
  ?substrand wdt:P921 ?item.
  ?substrand wdt:P17 wd:Q{country_code}.

  OPTIONAL {{ ?substrand wdt:P361 ?programa. }}
  OPTIONAL {{ ?articulo schema:about ?item;
    schema:isPartOf <https://{wikipedia_language_code}.wikipedia.org/>. 
    ?articulo schema:name ?nombreDelArticulo.
  }}

  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{wikipedia_language_code}". }}
}}
"""


def fetch_wikidata_info(wikipedia_language_code, country_code):
    # Wikidata endpoint URL for the SPARQL query
    wikidata_endpoint = "https://query.wikidata.org/sparql"
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])

    sparql_query = SPARQL_QUERY.format(wikipedia_language_code=wikipedia_language_code, country_code=country_code)

    sparql = SPARQLWrapper(wikidata_endpoint, agent=user_agent)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def store_articles(results, article_file):
    # Extract article names from results
    article_names = [result.get("nombreDelArticulo", {}).get("value", "") for result in results['results']['bindings']]
    # Remove empty names
    article_names = [name for name in article_names if name]
    # Sort article names alphabetically
    article_names.sort()
    # Write sorted article names to the file
    with open(article_file, "w", encoding="utf-8", errors="replace") as file:
        for article_name in article_names:
            file.write(f"{article_name}\n")


def get_id_and_subjects_and_grade(results, subject_file):
    with open(subject_file, "w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id_wikidata", "material", "grade"])
        for result in results['results']['bindings']:
            id_wikidata = result.get("qid", {}).get("value", "")
            material = result.get("programaLabel", {}).get("value", "")
            grade = result.get("programaLabel", {}).get("value", "")
            # Additional processing for grade and material
            # Write to CSV
            writer.writerow([id_wikidata, material, grade])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide both the wikipedia_language and country code as command-line arguments.")
        sys.exit(1)

    wikipedia_language_code = sys.argv[1]
    country_code = sys.argv[2]

    # Check if the language and country code combination is supported
    config_key = f"{wikipedia_language_code}_{country_code}"
    file_mapping = CONFIG.get(config_key)
    if not file_mapping:
        print("Unsupported language or country code.")
        sys.exit(1)

    article_file, subject_file = file_mapping['article_file'], file_mapping['subject_file']

    query_results = fetch_wikidata_info(wikipedia_language_code, country_code)
    store_articles(query_results, article_file)
    get_id_and_subjects_and_grade(query_results, subject_file)
