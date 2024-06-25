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
  VALUES ?item {{  wd:Q1003584 wd:Q1004920 wd:Q1005003 wd:Q1005742 wd:Q1006155 wd:Q1007576 wd:Q1010338 wd:Q10301134 wd:Q1043575 wd:Q1046409 wd:Q1046478 wd:Q1046504 wd:Q1050600 wd:Q1056025 wd:Q105994249 wd:Q106617776 wd:Q1078765 wd:Q108325 wd:Q1103148 wd:Q110722911 wd:Q112032693 wd:Q1133967 wd:Q1137902 wd:Q1139321 wd:Q113952708 wd:Q1142828 wd:Q1172515 wd:Q118680568 wd:Q11922443 wd:Q119824897 wd:Q119825899 wd:Q121758527 wd:Q123022508 wd:Q123144720 wd:Q123575748 wd:Q123895328 wd:Q123944210 wd:Q124048623 wd:Q124078824 wd:Q124079569 wd:Q124152271 wd:Q124152365 wd:Q124359432 wd:Q124810392 wd:Q124891094 wd:Q124949900 wd:Q124953365 wd:Q125270514 wd:Q125270526 wd:Q125270542 wd:Q125270569 wd:Q125270587 wd:Q125341719 wd:Q125372850 wd:Q125415439 wd:Q1273950 wd:Q1284536 wd:Q1284544 wd:Q1285687 wd:Q1313631 wd:Q1335 wd:Q13479688 wd:Q134916 wd:Q1363025 wd:Q136689 wd:Q1369351 wd:Q1413045 wd:Q1421671 wd:Q1438902 wd:Q1452181 wd:Q1485477 wd:Q1496532 wd:Q1516703 wd:Q1519373 wd:Q15262908 wd:Q15265512 wd:Q1549798 wd:Q1570788 wd:Q1574280 wd:Q1581250 wd:Q1630447 wd:Q1630975 wd:Q1632358 wd:Q16489268 wd:Q16489274 wd:Q16490184 wd:Q16534500 wd:Q16540315 wd:Q1655272 wd:Q16559143 wd:Q16606548 wd:Q16608928 wd:Q16619711 wd:Q16619735 wd:Q16628151 wd:Q16638146 wd:Q168204 wd:Q16932860 wd:Q170598 wd:Q1713700 wd:Q1726492 wd:Q1734134 wd:Q1749496 wd:Q177318 wd:Q18278 wd:Q18416046 wd:Q18416816 wd:Q18417023 wd:Q1851746 wd:Q187456 wd:Q1892879 wd:Q190492 wd:Q1921137 wd:Q192705 wd:Q19413 wd:Q20024877 wd:Q208281 wd:Q2094894 wd:Q2099102 wd:Q2099121 wd:Q21077366 wd:Q21224061 wd:Q2502590 wd:Q2529255 wd:Q2532143 wd:Q257698 wd:Q2722348 wd:Q28099627 wd:Q28170227 wd:Q283417 wd:Q28501882 wd:Q28946378 wd:Q29584874 wd:Q3001412 wd:Q3014645 wd:Q312164 wd:Q313531 wd:Q31996664 wd:Q31996693 wd:Q31996760 wd:Q31996899 wd:Q31996930 wd:Q31999878 wd:Q32292 wd:Q3303747 wd:Q335506 wd:Q3378208 wd:Q3442574 wd:Q34982 wd:Q35827 wd:Q367083 wd:Q3817491 wd:Q38720 wd:Q389478 wd:Q3947 wd:Q40080 wd:Q42382088 wd:Q4239995 wd:Q42963669 wd:Q42970217 wd:Q42970348 wd:Q42971413 wd:Q42971782 wd:Q42971983 wd:Q42972024 wd:Q42972429 wd:Q42972673 wd:Q42972867 wd:Q42972898 wd:Q42973198 wd:Q42973514 wd:Q42973538 wd:Q42974150 wd:Q42974490 wd:Q42974907 wd:Q42974977 wd:Q42976004 wd:Q42976965 wd:Q429785 wd:Q42979488 wd:Q42980423 wd:Q42981917 wd:Q42985880 wd:Q42991130 wd:Q42991215 wd:Q43326598 wd:Q471275 wd:Q475116 wd:Q48707 wd:Q4874218 wd:Q4891600 wd:Q49323020 wd:Q4970066 wd:Q498245 wd:Q503958 wd:Q508659 wd:Q5472521 wd:Q551848 wd:Q55579276 wd:Q55586368 wd:Q55988964 wd:Q56064 wd:Q56069 wd:Q56438160 wd:Q56605983 wd:Q5703703 wd:Q5740562 wd:Q5775039 wd:Q5795204 wd:Q5807917 wd:Q5854517 wd:Q5854823 wd:Q5855171 wd:Q5856541 wd:Q588205 wd:Q5902809 wd:Q5908539 wd:Q5908657 wd:Q5911337 wd:Q591367 wd:Q5926445 wd:Q5956468 wd:Q6062260 wd:Q6062262 wd:Q6092503 wd:Q6139719 wd:Q6139965 wd:Q6146584 wd:Q6160128 wd:Q6171774 wd:Q61865 wd:Q621114 wd:Q6406075 wd:Q657449 wd:Q6896221 wd:Q703047 wd:Q703300 wd:Q703332 wd:Q7139644 wd:Q7158469 wd:Q721226 wd:Q7260513 wd:Q7281352 wd:Q728478 wd:Q741103 wd:Q751376 wd:Q751982 wd:Q753853 wd:Q7609 wd:Q7811209 wd:Q786149 wd:Q790443 wd:Q7911864 wd:Q806192 wd:Q806203 wd:Q808953 wd:Q8338716 wd:Q844914 wd:Q849835 wd:Q859548 wd:Q891557 wd:Q9060872 wd:Q9064 wd:Q943708 wd:Q964094 wd:Q984180 wd:Q984193 wd:Q984382 wd:Q984388 wd:Q984390 wd:Q984425 wd:Q984427 wd:Q984511 wd:Q984873 wd:Q986346 wd:Q989939 }}  

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
