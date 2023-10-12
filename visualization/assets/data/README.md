## Running the Python Code

To execute the Python code, follow these steps:

1. Open a terminal or command prompt.

2. Navigate to the project directory where the Python script is located.

4. Run the 'add-grade.py' script with the following command:

`$ python add-grade.py`

This script will add the 'grade' column to the 'voci_2023.tsv' file based on the results of the SPARQL query.

##SPARQL Query

This SPARQL query retrieves unique instances of 'id_wikidata' and their corresponding 'programaLabel'.

The data is filtered based on the conditions specified in the query, such as being related to Uruguay (wd:Q77).

```sparql
SELECT DISTINCT ?id_wikidata ?programaLabel
WHERE {
  ?substrand wdt:P31 wd:Q600134.
  ?substrand wdt:P921 ?id_wikidata.
  ?substrand wdt:P17 wd:Q77. #Uruguay

  OPTIONAL { ?substrand wdt:P361 ?programa. }

  SERVICE wikibase:label { bd:serviceParam wikibase:language "es". }
}
```

Download the query to a TSV file.