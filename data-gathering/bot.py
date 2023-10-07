import urllib

import sys

import calendar

import json

import datetime

from urllib.request import urlopen

import urllib.parse

import string

import json

from datetime import datetime



# Function to get average page views: returns visits since the beginning of time, average dayly visits since the begininning of time, average daily visits in the specified year

def get_avg_pageviews(article, start_date, end_date, language):
   SUM = 0

   try:
      url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{language}.wikipedia/all-access/user/{article}/daily/{start_date}/{end_date}"
      html = urlopen(url).read()
      html = str(html)
      html = html.replace('{"items":[', "")
      html = html.replace(']}', "")
      n = html.count("}")

      for i in range(n):
         txt = html[:html.find("}") + 1]
         SUM += int(txt[txt.find('"views":') + len('"views":'): -1])
         html = html.replace(txt, "", 1)

      d1 = datetime.strptime(start_date, "%Y%m%d")
      d2 = datetime.strptime(end_date, "%Y%m%d")
      days = (abs((d2 - d1).days) + 1)
      result = str(int(round((SUM / days), 0)))
   except:
      result = "ERROR"

   return result



# Function to calculate visits
def visits(article, language, review=0):
   # Date formats
   START_ALL_TIME = "20150701"
   START_PREV_YEAR = "20220101"
   END_PREV_YEAR = "20221231"
   START_CURRENT_YEAR = "20230101"
   END_CURRENT_YEAR = "20230831"

   results = []

   #calculate ris1, total pageviews since the beginning of time, and ris2, average pageviews since de beginning of time

   try:
      d1 = datetime.strptime(START_ALL_TIME, "%Y%m%d")
      d2 = datetime.strptime(END_CURRENT_YEAR, "%Y%m%d")
      days = (abs((d2 - d1).days) + 1)
      article_encoded = urllib.parse.quote(article) # or article_encoded = article.replace(" ","_")

      # Calculate total page views since the beginning of time
      url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{language}.wikipedia/all-access/user/{article_encoded}/daily/{START_ALL_TIME}/{END_CURRENT_YEAR}"
      html = urlopen(url).read()
      html = str(html)

      if review == 0:
         html = html.replace('{"items":[', "")
         html = html.replace(']}', "")
         n = html.count("}")

         SUM = 0

         for i in range(n):
               txt = html[:html.find("}") + 1]
               SUM += int(txt[txt.find('"views":') + len('"views":'): -1])
               html = html.replace(txt, "", 1)

         total_page_views = str(SUM)
         average_page_views = str(int(round((SUM / days), 0)))
      else:
         total_page_views = "REVIEW"
         average_page_views = "REVIEW"

      # Calculate average page views from the previous year
      average_prev_year = get_avg_pageviews(article_encoded, START_PREV_YEAR, END_PREV_YEAR, language)

      # Calculate average page views from the current year
      average_current_year = get_avg_pageviews(article_encoded, START_CURRENT_YEAR, END_CURRENT_YEAR, language)

      results.extend([total_page_views, average_page_views, average_prev_year, average_current_year])
   except:
      results.extend(["ERROR", "ERROR", "ERROR", "ERROR"])

   return results



# Function to return ID of an item
def return_id(item):
   return item.getID()


# Function to count notes

#Thhis function counst the number of times the substring "</ref>" appears within the input string "text".
#It converts the count (which is an integer) into a string and returns the result as a string representing the count of occurrences of "</ref>" within the input string.
def count_notes(text):
    return str(text.count('</ref>'))


# Function to calculate and return the length of a given string as a string.
def calculate_size(text):
    return str(len(text))


# this function counts the occurrences of specific image file extensions within a given string and returns that count as a string.
def count_images(text):
    t = text.lower()
    img = str(
        t.count('.jpg') + t.count('.svg') + t.count('.jpeg') + t.count('.png') + t.count('.tiff') + t.count('.gif') + t.count(
            '.tif') + t.count('.xcf'))
    return img


# function relies on external web scraping 
# it reads the HTML content of the page and converts it's content to a string and then extracts a specific portion of the HTML using string manipulation. 
#Specifically, it looks for the substring "created_at" and extracts the following 10 characters, which should represent the creation date of the Wikipedia article.
def get_first_edit(voce, language):
    try:
        url = f"https://xtools.wmflabs.org/api/page/articleinfo/{language}.wikipedia.org/{voce.replace(" ","_")}"
        html = urlopen(url).read()
        html = str(html)
        html = html[html.find("created_at") + len("created_at") + 3:]
        html = html[:10]
    except:
        html = "ERROR"
    return html



# # This function analyzes and count specific types of tags within a given text. The results are returned as strings, making them suitable for further processing.
def count_warnings(t, language):
   t_tmp = t
   t = t.replace("\n", "")
   t = t.replace(" ", "")
   t = t.lower()
   # tmp  == template

   with open("language_templates.json", "r") as config_file:
      language_templates = json.load(config_file)


   tmp_to_check = sum(t.count(template) for template in language_templates["to_check"])
   tmp_synoptic = sum(t.count(template) for template in language_templates["synoptic"])
   tmp_help = sum(t.count(template) for template in language_templates["help"])
   tmp_correct = sum(t.count(template) for template in language_templates["correct"])
   tmp_curiosity = sum(t.count(template) for template in language_templates["curiosity"])
   tmp_divide = sum(t.count(template) for template in language_templates["divide"]) 
   tmp_sources = sum(t.count(template) for template in language_templates["sources"])
   tmp_localism = sum(t.count(template) for template in language_templates["localism"])
   tmp_pov = sum(t.count(template) for template in language_templates["pov"])
   tmp_nn = sum(t.count(template) for template in language_templates["nn"])
   tmp_recentism = sum(t.count(template) for template in language_templates["recentism"])
   tmp_manual_style = sum(t.count(template) for template in language_templates["manual_style"])
   tmp_translation = sum(t.count(template) for template in language_templates["translation"])
   tmp_wikificare = sum(t.count(template) for template in language_templates["wikificare"]) 
   tmp_stub = sum(t.count(template) for template in language_templates["stub"])
   tmp_stub_section = sum(t.count(template) for template in language_templates["stub_control"])
   tmp_copy_control = sum(t.count(template) for template in language_templates["copy_control"])

   sum_of_warnings = tmp_to_check + tmp_synoptic + tmp_help + tmp_correct + tmp_curiosity + tmp_divide + tmp_sources + tmp_localism + tmp_pov
   sum_of_warnings += tmp_nn + tmp_recentism + tmp_manual_style + tmp_translation + tmp_wikificare + tmp_stub + tmp_stub_section + tmp_copy_control


   tmp_without_sources = sum(t.count(template) for template in language_templates["without_sources"])
   tmp_to_clarify = sum(t.count(template) for template in language_templates["clarify"])

   return str(sum_of_warnings), str(tmp_without_sources), str(tmp_to_clarify)


#  this function parses and extracts templates from a larger text, allowing further analysis of the template content. 
def find_template(text):
    tmp = text[2:]
    tmp2 = text[2:]
    tmp = tmp[:tmp.find("}}") + 2]

    if "{{" in tmp:
        tmp3 = tmp[tmp.find("{{"):]
        tmp2 = tmp2.replace(tmp3, "$$$$$$$$$$$$$$")
        tmp2 = tmp2[:tmp2.find("}}") + 2]
        tmp2 = tmp2.replace("$$$$$$$$$$$$$$", tmp3)
        return tmp2
    return tmp



# Function to calculate the length of the introduction
#Incipit means the opening of a manuscript, early printed book. Hence, incipit == introduction 
def calculate_introduction_length(text):
   incipit = text
   incipit = incipit[:incipit.find("\n==")]
   template_count = incipit.count('{{')
   incipitclear = incipit
   format_num = incipit.count("{{formatnum:")


   for i in range(format_num):
      tmp = incipit[incipit.find("{{formatnum:"):]

      tmp = tmp[:tmp.find("}}") + 2]
      tmp2 = tmp.replace("{{formatnum:", "")
      tmp2 = tmp2.replace("}}", "")
      incipit = incipit.replace(tmp, tmp2)

   template_count = incipit.count("{{")

   for i in range(template_count):
      text = incipit[incipit.find("{{"):]

      template = find_template(text)
      text = text.replace("{{" + template, "")
      incipit = incipit.replace("{{"+template,"")

   incipit = incipit.replace("</ref>","")
   n = incipit.count("<ref")

   for i in range(n):
      tmp = incipit[incipit.find("<ref"):]

      tmp = tmp[:tmp.find(">") + 1]
      incipit = incipit.replace(tmp,"")

   incipit = incipit.replace("[[", "")
   incippit = incipit.replace("]]", "")
   incipit = incipit.replace("|", "")

   introduction_length = len(incipit)
   return str(introduction_length)



# Function to check if the article is a "good article"
def vdq(text, dispay_window_template):
    if dispay_window_template.lower() in text.lower(): #or if dispay_window_template in text.lower():
        return "1"
    else:
        return "0"
    


# Function to check if the article is a "featured article"    
def is_featured_article(text, featured_template):
    if featured_template.lower() in text.lower(): # or if featured_template in text.lower()
        return "1"
    else:
        return "0"


    
# Main analysis function
def analysis(language, dimension, first_edit, note, images, views, incipit_size,
            discussion_size, discussionURL, warnings_config, common_pages, common_gallery, 
            itwikisource, featured, coordinate):
                        
   f = open('query.csv', "r")
   lines = f.readlines()   
    
   #delete the contents of the file before starting
   results = open('resultati.txt',"w") #replace with txt file to be worked on
   results.truncate(0)
   results.close()

   for line in lines: 
      results = open('resultati.txt', 'a')  # open the file in append mode
      flag = 1
      line = line[:-1]
      line = line.replace(" ","_")
      result = ""
      wikitext = ""

      line2 = urllib.parse.quote(line)
      line = line.replace(" ","_")


      try:

        url = f"https://{language}.wikipedia.org/w/api.php?action=parse&page={line2}&prop=wikitext&formatversion=2&format=json"
        json_url = urlopen(url)
        data = json.loads(json_url.read())
        wikitext = data["parse"]["wikitext"]

        if "#REDIRECT"  in wikitext:
          line2 = wikitext[wikitext.find("[[")+2:]
          line2 = line2[:line2.find("]]")]
          line = line2
          line2 = line2.replace("_"," ")

      except:
        pass                                     

      try:
        line2 = urllib.parse.quote(line)
        line = line.replace(" ","_")
        url = "https://"+language+".wikipedia.org/w/api.php?action=query&titles=" + line2 +"&prop=pageprops&format=json&formatversion=2"
        json_url = urlopen(url)
        data = json.loads(json_url.read())
        wikidataid = data["query"]["pages"][0]["pageprops"]["wikibase_item"]
        url ="https://www.wikidata.org/wiki/Special:EntityData/"+wikidataid+".json"
        json_url = urlopen(url)

        wikidata = json.loads(json_url.read())


        url = "https://"+language+".wikipedia.org/w/api.php?action=parse&page=" + line2 + "&prop=wikitext&formatversion=2&format=json"
        json_url = urlopen(url)
        data = json.loads(json_url.read())
        wikitext = data["parse"]["wikitext"]

        try:

          url = "https://"+language+".wikipedia.org/w/api.php?action=parse&page=" + discussionURL + line2 + "&prop=wikitext&formatversion=2&format=json"
          json_url = urlopen(url)

          data = json.loads(json_url.read())

          wikitext_discussione = data["parse"]["wikitext"]

        except:
          wikitext_discussione = ""

        result = result + line + "\t"

        result = result + wikidataid + "\t"

      except:

        result = result + line +"\t" +"Voce inesistente"

       

      else:

        if first_edit:
           result = result + first_edit(line2) + "\t"

        if dimension:
           result = result + dimension(wikitext) + "\t"

        if images:
           result = result + images(wikitext) + "\t"

        if note:
           result = result + note(wikitext) + "\t"

        if warnings_config:
           for i in count_warnings(wikitext):
              print("some alerts")
              result = result + i + "\t"   

        if discussion_size:
           result = result + dimension(wikitext_discussione) + "\t"

        if incipit_size:
           result = result + calculate_introduction_length(wikitext) + "\t"
   

        if views:
           for i in visits(line2):
              result = result + i + "\t"

        if vdq:
           result = result + vdq(wikitext) + "\t"

        if featured:
           result = result + is_featured_article(wikitext) + "\t"


        if common_gallery:
           try:
              result = result + wikidata["entities"][wikidataid]["claims"]["P373"][0]["mainsnak"]["datavalue"]["value"] + "\t"
           except:
              result = result + "" + "\t"

        if common_pages:
           try:
              result = result + wikidata["entities"][wikidataid]["claims"]["P935"][0]["mainsnak"]["datavalue"]["value"] + "\t"

           except:
              result = result + "" + "\t"


        if itwikisource:
           try:
              result = result + wikidata["entities"][wikidataid]["sitelinks"]["itwikisource"]["title"] + "\t"

           except:
              result = result + "\t"



        if coordinate:

           try:

              result = result + wikidata["entities"][wikidataid]["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]["latitude"] + "\t"

              result = result + wikidata["entities"][wikidataid]["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]["longitude"] + "\t"

           except:

              result = result + "\t" + "\t"

      results.write(result + "\n")  # aggiungere un salto di linea dopo ogni risultato
      results.close()  # chiudere il file
      print (result)



# Open and read the JSON configuration file
with open("wikipedia_config.json", "r") as config_file:
   wikipedia_config = json.load(config_file)

#Now, you can access the configuration data as a dictionary


def main():
   # Specify the Wikipedia language
   wikipedia_language = "es"  # Change this to the desired Wikipedia language

   if wikipedia_language in wikipedia_config:
      language_config = wikipedia_config[wikipedia_language]
   else:
      print(f"Configuration not found for language '{wikipedia_language}'.") # Handle this case appropriately (e.g, exit the script).

    
   # Access configuration variables based on the language
   language = language_config.get("language")
   id_wikidata = language_config.get("id_wikidata")
   dimension_option = language_config.get("dimension")
   first_edit_option = language_config.get("first_edit") 
   note_option = language_config.get("note")
   images_option = language_config.get("images")
   views_option = language_config.get("views")
   incipit_size_option = language_config.get("incipit_size")
   discussion_size_option = language_config.get("discussion_size")
   discussionURL = language_config.get("discussionURL")
   warnings_config = language_config.get("warnings_config")
   common_pages_option = language_config.get("common_pages")
   common_gallery_option = language_config.get("common_gallery")
   itwikisource_option = language_config.get("itwikisource")
   wikiversity_option = language_config.get("wikiversity")
   wikibooks_option = language_config.get("wikibooks")
   feature_option = wikipedia_language("featured")
   quality_option = language_config.get("quality")
   review_option = language_config.get("review")
   bibliography_option = language_config.get("bibliography")
   coordinate_option = language_config.get("coordinate")
   featured_template = language_config.get("featured_template")
   dispay_window_template = language_config.get("dispay_window_template")

   # Call your analysis function or other code logic here, passing the parameters
   analysis(
      language = language,
      id_wikidata = id_wikidata,
      dimension = dimension_option,
      first_edit = first_edit_option,
      note = note_option,
      images = images_option,
      views = views_option,
      incipit_size = incipit_size_option,
      discussion_size = discussion_size_option,
      discussionURL = discussionURL,
      warnings_config = warnings_config,
      common_pages = common_pages_option,
      common_gallery = common_gallery_option,
      itwikisource = itwikisource_option,
      wikiversity = wikiversity_option,
      wikibooks = wikibooks_option,
      featured = feature_option, 
      quality = quality_option,
      review = review_option,
      bibliography = bibliography_option,
      coordinate = coordinate_option,
      featured_template = featured_template,
      dispay_window_template = dispay_window_template,
   )

if __name__ == "__main__":
    main()
