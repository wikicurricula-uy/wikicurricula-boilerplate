'''
This script is for producing the configuration files; "language_template_config.json"
and "wikipwdia_config.js" for parameterization.
'''



import json
import urllib.parse

# Define a dictionary or configuration file for each Wikipedia language
discussion = "Discusión:"
wikipedia_config = {
    "es": {  #for spanish
         "language": "es",
         "utf_required": "utf-8",
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
         "commons_pages": 1,
         "commons_gallery": 1,
         "itwikisource": 1,
         "wikiversity": 1,
         "wikibooks": 1,
         "featured_in": 1,
         "quality": 1,
         "review": 1,
         "bibliography": 1,
         "coordinate": 1,
         "featured_template": "{{artículo destacado",  # display_window Template
         "display_window_template": "{{artículo bueno",  # Quality Template
      },
    "it": {   #for italian
         "language": "it",
         "utf_required": "utf-8",
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
         "commons_pages": 1,
         "commons_gallery": 1,
         "itwikisource": 1,
         "wikiversity": 1,
         "wikibooks": 1,
         "featured_in": 1,
         "quality": 1,
         "review": 1,
         "bibliography": 1,
         "coordinate": 1,
         "featured_template": "{{voce in vetrina",  # display_window Template (Italian)
         "display_window_template": "{{voce buona",  # Quality Template (Italian)
      },
    "en": { #for english
        "language": "en",
         "utf_required": "utf-8",
         "id_wikidata": 1,
         "dimension": 1,
         "first_edit": 1,
         "note": 1,
         "images": 1,
         "views": 1,
         "incipit_size": 1,
         "discussion_size": 1,
         "discussionURL": urllib.parse.quote("talk:"),  # Discussion Page Prefix
         "warnings_config": 0,
         "commons_pages": 1,
         "commons_gallery": 1,
         "itwikisource": 1,
         "wikiversity": 1,
         "wikibooks": 1,
         "featured_in": 1,
         "quality": 1,
         "review": 1,
         "bibliography": 1,
         "coordinate": 1,
         "featured_template": "{{featured article",  # display_window Template (English)
         "display_window_template": "{{good article",  # Quality Template (English)
      },

      # "tw": {  #for Twi, a ghanian language: To be configured later
      #   "language": "en",
      #    "utf_required": "utf-8",
      #    "id_wikidata": 1,
      #    "dimension": 1,
      #    "first_edit": 1,
      #    "note": 1,
      #    "images": 1,
      #    "views": 1,
      #    "incipit_size": 1,
      #    "discussion_size": 1,
      #    "discussionURL": urllib.parse.quote("talk:"),  # Discussion Page Prefix
      #    "warnings_config": 0,
      #    "commons_pages": 1,
      #    "commons_gallery": 1,
      #    "itwikisource": 1,
      #    "wikiversity": 1,
      #    "wikibooks": 1,
      #    "featured_in": 1,
      #    "quality": 1,
      #    "review": 1,
      #    "bibliography": 1,
      #    "coordinate": 1,
      #    "featured_template": "{{featured article",  # display_window Template (English)
      #    "display_window_template": "{{good article",  # Quality Template (English)
      # },
      # Add configurations for other Wikipedia languages as needed
}

language_template_config = {
    "en": {
    "to_check": ["{{verifiability|", "{{verifiability}}"],
    "synoptic": ["{{infobox requested|", "{{infobox requested}}"],
    "correct": ["{{copy edit"],
    "curiosity": ["{{trivia|", "{{trivia}}"],
    "divide": ["{{split|", "{{split}}"],
    "sources": ["{{unreferenced|", "{{unreferenced}}"],
    "localism": ["{{globalize|", "{{globalize}}"],
    "pov": [ "{{POV|", "{{POV}}"],
    "nn": ["{{no footnotes|", "{{no footnotes}}"],
    "recentism": ["{{recentism}}"],
    "manual_style": [],
    "translation": ["{{not English}}"],
    "wikificare": ["{{wikify|", "{{wikify}}"],
    "stub": ["{{stub|", "{{stub}}"],
    "stub_section": ["{{expand section"],
    "copy_control": ["{{cv-unsure"],
    "without_sources": ["{{unreferenced}}", "{{citation needed}}"],
    "clarify": ["{{clarify}}"]
    },

#  "tw": {
#     "to_check": ["{{cleanup}}"],
#     "synoptic": ["{{tmp|", "{{tmp}}"],
#     "correct": ["{{correct}}"],
#     "curiosity": ["{{curiosity}}"],
#     "divide": ["{{divide|", "{{divide}}"],
#     "sources": ["{{sources|", "{{sources}}"],
#     "localism": ["{{localism|", "{{localism}}"],
#     "pov": ["{{pov|", "{{pov}}"],
#     "nn": ["{{nn|", "{{nn}}"],
#     "recentism": ["{{recentism}}"],
#     "manual_style": ["{{manual style}}"],
#     "translation": ["{{translation}}"],
#     "wikificare": ["{{wikificare|", "{{wikificare}}"],
#     "stub": ["{{stub|", "{{stub}}"],
#     "stub_section": ["{{stub section}}"],
#     "copy_control": ["{{control copy}}"],
#     "without_sources": ["{{unreferenced}}", "{{citation needed}}"],
#     "clarify": ["{{clarify}}"]
#   },
  "es": {
    "to_check": [],
    "synoptic": [],
    "correct": ["{{copyedit"],
    "curiosity": ["{{curiosidades}}"],
    "divide": ["{{separar"],
    "sources": ["{{referencias|"],
    "localism": ["{{globalizar|"],
    "pov": ["{{no neutralidad|", "{{no neutralidad}}"],
    "nn": ["{{notas al pie|", "{{notas al pie}}"],
    "recentism": ["{{recentismo"],
    "manual_style": ["{{mejorar redacción"],
    "translation": ["{{traducción incompleta"],
    "wikificare": ["{{wikificar"],
    "stub": [],
    "stub_section": [],
    "copy_control": [],
    "without_sources": ["{{sinreferencias", "{{sin referencias", "{{cita requerida"],
    "clarify": [ "{{qué",
            "{{cuál",
            "{{cuándo",
            "{{cuántos",
            "{{dónde",
            "{{quién"
          ]
  },
  "it":{
    "to_check": ["{{c|", "{{c}}"],
    "synoptic": ["{{tmp|", "{{tmp}}"],
    "correct": ["{{correggere"],
    "curiosity": ["{{curiosità"],
    "divide": ["{{d|", "{{d}}"],
    "sources": ["{{f|", "{{f}}"],
    "localism": ["{{l|", "{{l}}"],
    "pov": ["{{p|", "{{p}}"],
    "nn": ["{{nn|", "{{nn}}"],
    "recentism": ["{{recentismo"],
    "manual_style": ["{{stilemanualistico"],
    "translation": ["{{t|", "{{t}}"],
    "wikificare": ["{{w|", "{{w}}"],
    "stub": ["{{s|", "{{s}}"],
    "stub_section": ["{{s sezione"],
    "copy_control": ["{{controlcopy"],
    "without_sources": ["{{senza fonte",
            "{{senza fonte}}",
            "{{citazione necessaria",
            "{{citazione necessaria}}"],
    "clarify": ["{{chiarire", "{{chiarire}}"]
  },
    # Add more languages as required
}



# Serialize the data to JSON
json_data = json.dumps(wikipedia_config, indent=4, ensure_ascii=False)
language_json_data = json.dumps(language_template_config, indent=4, ensure_ascii=False)
# Write the JSON data to a file
with open("wikipedia_config.json", "w", encoding='utf-8') as json_file:
    json_file.write(json_data)
with open("language_template_config.json", "w", encoding='utf-8') as json_file:
    json_file.write(language_json_data)


# This code will create a JSON file named "wikipedia_config.json" with the provided data. 
# You can add configurations for other Wikipedia languages as needed by extending the wikipedia_config dictionary
