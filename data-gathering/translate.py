#this script translates all countries results.txt into a file that is readable by wikicurricula or wikiscuola visualization tool
import csv
import os
from datetime import datetime
import sys
import json

# Load configuration from JSON file
with open("wikipedia_config.json", "r") as config_file:
    CONFIG = json.load(config_file)

#This function calculates the number of days between two given date strings.
#It first converts the date strings into datetime objects and then calculates the difference in days between them.
def get_days_between(start_date_str, end_date_str):
    if (not start_date_str or start_date_str =="ERROR" or end_date_str =="ERROR"): return 0
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    days_between = (end_date - start_date).days
    return days_between


#This function calculates the ratio of the size of an incipit (usually the introductory part of an article) to the total size of an article.
#It's used to determine what percentage of the article size is occupied by the incipit.
def get_incipit_on_size(incipit_size,size):
    if (not incipit_size or not size): return 0; 
    return round((int(incipit_size) / int(size))*100,2)


#This function creates a subject mapping dictionary based on data from a specified CSV file.
#It reads the file and associates Wikidata IDs with their corresponding subjects, forming a mapping that can be used to categorize articles by subject.   
def create_subject_mapping(file_path):
    id_subject_map = {}

    # open file with id subject pairs in read mode
    with open(file_path, 'r',  encoding='utf-8', errors="replace") as file:
        reader = csv.reader(file, delimiter=',')
        header = next(reader, None)

        for row in reader:
            id_subject_map[row[0]] = row[1].strip()

    return id_subject_map

def create_grade_mapping(file_path):
    id_grade_map = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        header = next(reader, None)
        for row in reader:
            id_grade_map[row[0]] = row[2].strip()
    return id_grade_map



def process_input_file(input_file, output_file, subject_file):
    grade_map = create_grade_mapping(subject_file)
    subject_map = create_subject_mapping(subject_file); 



    # Open the input file
    with open(input_file, 'r',  encoding='utf-8', errors="replace") as input_file:

        input_header = [
            'article',
            'id_wikidata',
            'first_edit',
            'size',
            'images',
            'notes',
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
                'grade': grade_map.get(row['id_wikidata']),
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
                'issues': '0',
                'issues_prev': '-',
                'issue_sourceNeeded': '0',
                'issue_clarify': '0',
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
        

  # Open the file in write mode with encoding and newline settings
    with open(output_file, 'w', encoding='utf-8', newline='') as output_file:
   
        output_file.truncate(0) # This line clears the content of the file
   
        writer = csv.DictWriter(output_file, fieldnames=new_row.keys(), delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)


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

    input_file, output_file_path, subject_file = file_mapping['result_file'], os.path.abspath(file_mapping['output_file_path']), file_mapping['subject_file']
    process_input_file(input_file, output_file_path, subject_file)
