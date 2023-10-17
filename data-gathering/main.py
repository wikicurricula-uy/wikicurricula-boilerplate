import sys
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """
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


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

# To get the result of other variables like qid, item, itemLabel, and programaLabel
# for result in results["results"]["bindings"]:
#     item_Label = result["itemLabel"]["value"]
#     print(item_Label)
   

# To get the result of other the article name variable since it's case sensitive
for result in results["results"]["bindings"]:
    # Check if the variable name is 'nombreDelArticulo' or 'nombreDelarticulo'
    if 'nombreDelArticulo' in result:
        article_name = result["nombreDelArticulo"]["value"]
    elif 'nombreDelarticulo' in result:
        article_name = result["nombreDelarticulo"]["value"]
    else:
        article_name = "N/A"  # If the variable name is not found, set to 'N/A'

    print(article_name)