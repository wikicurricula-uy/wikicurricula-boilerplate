import pandas as pd

"""
SELECT DISTINCT ?id_wikidata ?programaLabel
WHERE {
  ?substrand wdt:P31 wd:Q600134.
  ?substrand wdt:P921 ?id_wikidata.
  ?substrand wdt:P17 wd:Q77. #Uruguay

  OPTIONAL { ?substrand wdt:P361 ?programa. }

  SERVICE wikibase:label { bd:serviceParam wikibase:language "es". }
}
"""

# This query was executed and the results were downloaded as the 'resultados.tsv' file.

# Read the data from the SPARQL query and store it in a DataFrame
resultados_df = pd.read_csv('../data/resultados.tsv', delimiter='\t')

# Read data from the 'voci_2023.tsv' file
voci_df = pd.read_csv('../data/voci_2023.tsv', delimiter='\t')

# Perform a merge based on the 'id_wikidata' column
voci_df = pd.merge(voci_df, resultados_df[['id_wikidata', 'programaLabel']], on='id_wikidata', how='left')

# Rename the 'programaLabel' column to 'grade'
voci_df = voci_df.rename(columns={'programaLabel': 'grade'})

# Save the resulting DataFrame back to a 'voci_2023.tsv' file with the new 'grade' column
voci_df.to_csv('voci_2023.tsv', sep='\t', index=False)

