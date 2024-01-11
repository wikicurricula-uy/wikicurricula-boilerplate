import csv
import sys
from SPARQLWrapper import SPARQLWrapper,JSON


if len(sys.argv) < 3:
  print("Please provide both the language and country code as command-line arguments.")
  sys.exit(1)

language = sys.argv[1]
code = sys.argv[2]

# TO-DO:  language-country interactions


if language == "en":
  article_file = "ghana_en_article_file.csv"
  subject_file = "ghana_en_subject_file.csv"
elif language == "es":
  article_file = "uruguay_es_article_file.csv"
  subject_file = "uruguay_es_subject_file.csv"
elif language == "tw":
  article_file = "ghana_tw_article_file.csv"
  subject_file = "ghana_tw_subject_file.csv"
else:
  print("Unsupported language.")
  sys.exit(1)



# SPARQL query to get information about specified country's national curriculum
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


# make a request to wikidata API to fetch Country's curriculum
def fetch_wikidata_info(language,code):
      # Wikidata endpoint URL for the SPARQL query
    wikidata_endpoint = "https://query.wikidata.org/sparql"
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
    with open(article_file, "w", encoding="utf-8", errors="replace") as file:
        for article_name in article_names:
            file.write(f"{article_name}\n")


# save subject and id of articles in respective subjects_file
def get_id_and_subjects_and_grade(results):
    with open(subject_file, "w") as file:
      file.truncate(0) # This line clears the content of the file

    with open(subject_file, "a", encoding="utf-8") as file:
      fields = ["id_wikidata", "material", "grade"]
      writer = csv.DictWriter(file, fieldnames=fields, lineterminator='\n')
      writer.writeheader()

      for result in results['results']['bindings']:
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

          if "Biología" in material or "biología" in material:
            material = "Biología"

          if "Física" in material:
            material = "Física"

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

          if "Geografía" in material or "geografía" in material:
            material = "Geografía"


          if "Educación musical" in material or  "Educación Musical" in material:
            material = "Educación musical"

          if "Comunicación Visual" in material or "Comunicación visual" in material:
            material = "Comunicación visual"

          if "Formación para la ciudadanía" in material:
            material = "Formación para la ciudadanía"

          if "Educación física y recreación" in material:
            material = "Educación física y recreación"

          #Let's map the to either Biología or Geografía
          #if "Ciencias del Ambiente" in material or "Ciencias del ambiente" in material:
          #  material = "Ciencias del ambiente"

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
  query_results = fetch_wikidata_info(language, code)
  store_articles(query_results)
  get_id_and_subjects_and_grade(query_results)
