import json
import urllib.parse

# Define a dictionary or configuration file for each Wikipedia language
discussion = "Discusión:"
wikipedia_config = {
    "es": {
         "language": "es",
         "id_wikidata": 1,
         "dimension": 1,
         "first_edit": 1,
         "note": 1,
         "images": 1,
         "views": 1,
         "incipit_size": 1,
         "discussion_size": 1,
         "discussionURL": urllib.parse.quote("discusión:"),  # Discussion Page Prefix
         "warnings_config": 0,
         "common_pages": 1,
         "common_gallery": 1,
         "itwikisource": 1,
         "wikiversity": 1,
         "wikibooks": 1,
         "featured": 1,
         "quality": 1,
         "review": 1,
         "bibliography": 1,
         "coordinate": 1,
         "featured_template": "{{artículo destacado",  # display_window Template
         "display_window_template": "{{artículo bueno",  # Quality Template
      },
    "it": {
         "language": "it",
         "id_wikidata": 1,
         "dimension": 1,
         "first_edit": 1,
         "note": 1,
         "images": 1,
         "views": 1,
         "incipit_size": 1,
         "discussion_size": 1,
         "discussionURL": urllib.parse.quote("discussione:"),  # Discussion Page Prefix
         "warnings_config": 0,
         "common_pages": 1,
         "common_gallery": 1,
         "itwikisource": 1,
         "wikiversity": 1,
         "wikibooks": 1,
         "featured": 1,
         "quality": 1,
         "review": 1,
         "bibliography": 1,
         "coordinate": 1,
         "featured_template": "{{voce in vetrina",  # display_window Template (Italian)
         "display_window_template": "{{voce buona",  # Quality Template (Italian)
      },
    "en": {
         "language": "en",
         "id_wikidata": 1,
         "dimension": 1,
         "first_edit": 1,
         "note": 1,
         "images": 1,
         "views": 1,
         "incipit_size": 1,
         "discussion_size": 1,
         "discussionURL": urllib.parse.quote("discussion:"),  # Discussion Page Prefix
         "warnings_config": 0,
         "common_pages": 1,
         "common_gallery": 1,
         "itwikisource": 1,
         "wikiversity": 1,
         "wikibooks": 1,
         "featured": 1,
         "quality": 1,
         "review": 1,
         "bibliography": 1,
         "coordinate": 1,
         "featured_template": "{{featured article",  # display_window Template (English)
         "display_window_template": "{{good article",  # Quality Template (English)
      },
      # Add configurations for other Wikipedia languages as needed
}



# Serialize the data to JSON
json_data = json.dumps(wikipedia_config, indent=4, ensure_ascii=False)

# Write the JSON data to a file
with open("wikipedia_config.json", "w", encoding='utf-8') as json_file:
    json_file.write(json_data)


# This code will create a JSON file named "wikipedia_config.json" with the provided data. 
# You can add configurations for other Wikipedia languages as needed by extending the wikipedia_config dictionary