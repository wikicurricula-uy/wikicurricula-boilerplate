#this script translates results.txt into a file that is readable by wikicurricula or wikiscuola visualization tool
import csv
from datetime import datetime

def get_days_between(start_date_str, end_date_str):
    if (not start_date_str or start_date_str =="ERRORE" or end_date_str =="ERRORE"): return 0
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    days_between = (end_date - start_date).days
    return days_between

def get_incipit_on_size(incipit_size,size):
    if (not incipit_size or not size): return 0;
    return round((int(incipit_size) / int(size))*100,2)

# maps a subject to and id
def create_subject_mapping(file_path):
    id_subject_map = {}

    # open file with id subject pairs in read mode
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        # skip reading the header
        header = next(reader, None)

        # each row is in the form Qid, subject. So create a dictionary with id keys and subject values. id_subject_map = {"Qid":English}
        for row in reader:
            id_subject_map[row[0]] = row[1].strip()

    return id_subject_map

subject_map = create_subject_mapping("subjects.csv");

# Open the input file
with open('resultati.txt', 'r', encoding='latin-1') as input_file:

    input_header = [
        'article',
        'id_wikidata',
        'first_edit',
        'size',
        'images',
        'notes',
        'issues',
        'issue_sourceNeeded',
        'issue_clarify',
        'discussion_size',
        'incipit_size',
        'all_visits',
        'avg_pv_all_time',
        'avg_pv_prev',
        'avg_pv',
        'vetrina',
        'VdQ',
        'commonsGallerys',
        'commonsPage',
        'page_on_wikisource'
    ]
    
    reader = csv.DictReader(input_file, fieldnames=input_header, delimiter='\t')

    # Create a list to store the rows
    rows = []

    # Iterate over the rows in the input file
    for row in reader:
        # Reorder the columns and replace missing values with zeros
        new_row = {
            'id_wikidata': row['id_wikidata'].replace("_", " "),
            'article': row['article'],
            'subject': subject_map.get(row['id_wikidata']),
            'avg_pv': row['avg_pv'],
            'avg_pv_prev': row['avg_pv_prev'],
            'size': row['size'],
            'size_prev': '-',
            'notes': row['notes'],
            'notes_prev': '-',
            'images': row['images'],
            'images_prev': '-',
            'references': '0',
            'references_prev': '-',
            'incipit_size': row['incipit_size'],
            'incipit_on_size': get_incipit_on_size(row['incipit_size'],row['size']),
            'incipit_prev': '-',
            'issues': row['issues'],
            'issues_prev': '-',
            'issue_sourceNeeded': row['issue_sourceNeeded'],
            'issue_clarify': row['issue_clarify'],
            'discussion_size': row['discussion_size'],
            'discussion_prev': '-',
            'first_edit': row['first_edit'],
            'days': get_days_between(row['first_edit'], '2022-12-31'),
            'all_visits': row['all_visits'],
            'VdQ': row['VdQ'],
            'vetrina': row['vetrina'],
            'commonsGallerys': row['commonsGallerys'],
            'commonsPage': row['commonsPage'],
            'page_on_wikisource': row['page_on_wikisource']
        }
        rows.append(new_row)
        
# Open the output file and write the reordered rows
    with open('../visualization/assets/data/voci_2023.tsv', 'a', encoding='utf-8', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=new_row.keys(), delimiter='\t')
            writer.writeheader()
            writer.writerows(rows)