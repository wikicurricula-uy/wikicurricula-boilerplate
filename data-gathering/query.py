'''
This script makes a call to the wikidata API by taking in the language_code, e.g "en" as an argument.
The result(data) of this query is then processed to get the artcle name, id and material of the articles into "article_name.csv" and "subjects.csv" files. 
The two(2) csv files produced canbe further used for analysis by the bot.py and for visualization.
'''

import csv
import requests
import sys  #Import the sys module to access command-line arguments

# Check if the language code is provided as a command-line argument
if len(sys.argv) > 1:
    WIKIPEDIA_LANGUAGE  = sys.argv[1]
else:
    WIKIPEDIA_LANGUAGE = "en"  # Default to "en" if no argument is provided


# add sparql query for other country's curriculum
if WIKIPEDIA_LANGUAGE== "en":
    sparql_query ="""
    SELECT DISTINCT (STRAFTER(STR(?item), "http://www.wikidata.org/entity/") AS ?qid) ?item ?itemLabel ?nombreDelArticulo ?programaLabel
    WHERE {
      ?substrand wdt:P31 wd:Q600134.
      ?substrand wdt:P921 ?item.
      ?substrand wdt:P17 wd:Q117. #Uruguay
      OPTIONAL { ?substrand wdt:P361 ?programa. }
      OPTIONAL { ?articulo schema:about ?item;
        schema:isPartOf <https://en.wikipedia.org/>. 
        ?articulo schema:name ?nombreDelArticulo.
      }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """
    article_file = "ghana_article_file.csv"
    subject_file = "ghana_subject_file.csv"

elif WIKIPEDIA_LANGUAGE == "es":
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
    article_file = "uruguay_article_file.csv"
    subject_file = "uruguay_subject_file.csv"



# make a request to wikidata API to fetch Ghana's curriculum
def fetch_wikidata_info():
    # Wikidata endpoint URL for the SPARQL query
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


# save article name in respective article_file
def get_articles(results):
    # Open the file in write mode to clear its contents
    with open(article_file, "w") as file:
        file.truncate(0) # This line clears the content of the file
        

    # Open the file in append mode and write data for each result
    with open(article_file, "a", encoding="utf-8") as file:
        for result in results:
            article_name = result.get("nombreDelArticulo", {}).get("value", "")
            if article_name != "":
                file.write(f"{article_name}\n")


# save subject and id of articles in respective subjects_file
def get_id_and_subjects_and_grade(results):
    with open(subject_file, "w") as file:
        file.truncate(0) # This line clears the content of the file
    with open(subject_file, "a", encoding="utf-8") as file:
        fields = ["id_wikidata", "material", "grade"]
        writer = csv.DictWriter(file, fieldnames=fields, lineterminator='\n')

        writer.writeheader()

        for result in results:
            id_wikidata = result.get("qid", {}).get("value", "")
            material = result.get("programaLabel", {}).get("value", "")
            grade = result.get("programaLabel", {}).get("value", "")


            if "7" in grade:
                grade = "7"
            
            if "8" in grade:
                grade = "8"

            if "9" in grade:
                grade = "9"

            if "Core" in grade:
                grade = "core"
            
            if "Salud y Sexualidad" in material:
                material = "Salud y sexualidad"
            
            if "Programa de " in material:

                if "Lengua Española" in material:
                    material = "Lengua española"

                if "Literatura" in material:
                    material = "Literatura"

                if "Biología" in material:
                    material = "Biología"

                if "Física" in material:
                    material = "física"

                if "Historia" in material:
                    material = "Historia"

                if "Tecnologías" in material:
                    material = "Tecnologías"
                
                if "Matemática" in material:
                    material = "Matemática"

                if "Ciencias Físico-Químicas" in material:
                    material = "Ciencias físico-químicas"

                if "Química" in material:
                    material = "Química"

                if "Geografía" in material:
                    material = "Geografía"


                if "Educación musical" in material or  "Educación Musical" in material:
                    material = "Educación musical"

                if "Comunicación Visual" in material or "Comunicación visual" in material:
                    material = "Comunicación visual"

                if "Formación para la ciudadanía" in material:
                    material = "Formación para la ciudadanía"

                if "Educación física y recreación" in material:
                    material = "Educación física y recreación"

                if "Ciencias del Ambiente" in material or "Ciencias de la computación" in material:
                    material = "Ciencias del ambiente"

                if "Ciencias de la computación" in material or "Ciencias de la Computación" in material:
                    material = "Ciencias de la computación"

                if "Comunicación y sociedad" in material:
                    material = "Comunicación y sociedad"

                if "Comunicación Visual y diseño" in material:
                    material = "Comunicación visual y diseño"
                
                if "Diseño" in material:
                    material = "Diseño"

                if "Comunicación Visual" in material:
                    material = "Comunicación Visual"
                    

            if "Curriculum" in material:
                material = material.split("Curriculum")[0]

                        
            if "Science" in material:
                material = "Science"
            
            writer.writerow({"id_wikidata": id_wikidata, "material": material, "grade": grade})

if __name__ == "__main__":
    query_result = fetch_wikidata_info()
    get_articles(query_result)
    get_id_and_subjects_and_grade(query_result)
    