import json
import csv
import sys
from SPARQLWrapper import SPARQLWrapper, JSON

# Load configuration from JSON file
with open("wikipedia_config.json", "r") as config_file:
    CONFIG = json.load(config_file)

# SPARQL query template
SPARQL_QUERY = """
SELECT DISTINCT (STRAFTER(STR(?item), "http://www.wikidata.org/entity/") AS ?qid) ?item ?itemLabel ?nombreDelArticulo ?programaLabel
WHERE {{
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{wikipedia_language_code},en". }}
  
  #terms in UdeSA's list
  VALUES ?item {{ wd:Q22661680 wd:Q2685659 wd:Q116003889 wd:Q260607 wd:Q396338 wd:Q113330288 wd:Q2855609 wd:Q26841 wd:Q5659642 wd:Q841083 wd:Q841083 wd:Q6135446 wd:Q7942 wd:Q125928 wd:Q79995 wd:Q2982731 wd:Q212254 wd:Q20113959 wd:Q10480147 wd:Q954112 wd:Q58734 wd:Q20051297 wd:Q839399 wd:Q60933643 wd:Q169940 wd:Q1334780 wd:Q838577 wd:Q296486 wd:Q497743 wd:Q948732 wd:Q924713 wd:Q48782631 wd:Q4116742 wd:Q12705 wd:Q548599 wd:Q167336 wd:Q3104563 wd:Q180388 wd:Q983063 wd:Q310667 wd:Q2022868 wd:Q1291678 wd:Q5956792 wd:Q27999483 wd:Q43619 wd:Q111494758 wd:Q898653 wd:Q266462 wd:Q386426 wd:Q4572 wd:Q6077659 wd:Q919526 wd:Q2144359 wd:Q132580 wd:Q936791 wd:Q1138571 wd:Q815818 wd:Q283509 wd:Q17072637 wd:Q11945323 wd:Q846574 wd:Q1361172 wd:Q10372857 wd:Q7552762 wd:Q1364792 wd:Q219416 wd:Q6135446 wd:Q795757 }}  

  OPTIONAL {{ ?articulo schema:about ?item;
    schema:isPartOf <https://{wikipedia_language_code}.wikipedia.org/>. 
    ?articulo schema:name ?nombreDelArticulo.
  }}
  
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
    # Use a set to store unique article names
    unique_article_names = set(article_names)
    # Convert the set to a sorted list
    sorted_unique_article_names = sorted(unique_article_names)
    # Write sorted unique article names to the file
    with open(article_file, "w", encoding="utf-8", errors="replace") as file:
        for article_name in sorted_unique_article_names:
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
            if "7" in grade:
                grade = "7"
                
            if "8" in grade:
                grade = "8"

            if "9" in grade:
                grade = "9"

            if "Core" in grade:
                grade = "core"
                
            if "Scuole superiori italiane" in grade:
                grade ="Scuole superiori italiane"
            if "scuola media italiana" or "escuela secundaria italiana" in grade:
                grade = "scuola media italiana"
            if "Scuola primaria italiana" in grade:
                grade = "Scuola primaria italiana"
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
                    
            if "Programma di " or "Programa de" in material:

                if "storia per" in material:
                    material = "Storia"
                if "grammatica italiana" in material:
                    material = "Grammatica Italiana"
                if "matematica e geometria" in material or "Matematica e Geometria" in material:
                    material = "Matematica e Geometria"
                if "musicale" in material:
                    material = "Musica"
                if "scienze per" in material:
                    material = "Scienze"
                if "Scienze e Tecnologie" in material:
                    material = "Scienze e Tecnologia"
                if "Educazione Civica" in material:
                    material = "Educazione Civica"
                if "Informatica" in material:
                    material = "Informatica"
                if "grammatica latina" in material:
                    material = "Grammatica Latina"
                if "biologia" in material:
                    material = "Biologia"
                if "chimica" in material:
                    material = "Chimica"
                if " Diritto ed Economia" in material or"diritto ed economia" in material:
                    material = "Diritto ed Economia"
                if "filosofia" in material:
                    material = "Filosofia"
                if "fisica" in material:
                    material = "Fisica"
                if "literatura italiana"in material:
                    material = "Literatura Italiana"
                
                if "storia dell'arte" in material:
                    material = "Storia dell'arte"

            if "Curriculum" in material:
                material = material.split("Curriculum")[0]

                            
            if "Science" in material:
                material = "Science"
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
