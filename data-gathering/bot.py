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



# Function to convert name to QID
def name_to_qid(item):
   return item.getID()


# Function to count notes
def count_notes(text):
    return str(text.count('</ref>'))


# Function to calculate size/dimension
def calculate_size(text):
    return str(len(text))


# Function to count images
def count_images(text):
    t = text.lower()
    img = str(
        t.count('.jpg') + t.count('.svg') + t.count('.jpeg') + t.count('.png') + t.count('.tiff') + t.count('.gif') + t.count(
            '.tif') + t.count('.xcf'))
    return img


# Function to get the first edit date
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



# Function to count warnings
def count_warnings(text):
    t_tmp = text
    t = t.replace("\n", "")
    t = t.replace(" ", "")
    t = t.lower()
   # tmp  == template
    tmp_to_check = t.count('{{c|') + t.count('{{c}}')
    tmp_synoptic = t.count('{{tmp|') + t.count('{{tmp}}')
    tmp_to_help = t.count('{{a|')
    tmp_to_correct = t.count('{{correggere')
    tmp_curiosity = t.count('{{curiosit')
    tmp_to_divide = t.count('{{d|') + t.count('{{d}')
    tmp_sources = t.count('{{f|') + t.count('{{f}}')
    tmp_localism = t.count('{{l|') + t.count('{{l}}')
    tmp_pov = t.count('{{p|') + t.count('{{p}}')
    tmp_nn = t.count('{{nn|') + t.count('{{nn}}')
    tmp_precentism = t.count('{{recentismo')
    tmp_manual_style = t.count('{{stilemanualistico')
    tmp_translation = t.count('{{t|') + t.count('{{t}}')
    tmp_wikificare = t.count('{{w|') + t.count('{{w}}')
    tmp_stub = t.count('{{s|') + t.count('{{s}}')
    tmp_stub_section = t.count('{{stubsezione')
    tmp_copy_control = t.count('{{controlcopy')

    sum_of_warnings = tmp_to_check + tmp_synoptic + tmp_to_help + tmp_to_correct + tmp_curiosity + tmp_to_divide + tmp_sources + tmp_localism + tmp_pov
    sum_of_warnings += tmp_nn + tmp_precentism + tmp_manual_style + tmp_translation + tmp_wikificare + tmp_stub + tmp_stub_section + tmp_copy_control

    tmp_without_sources = t.count('{{senzafonte') + t.count('{{citazionenecessaria') + t.count('{{senzafonte}}') + t.count('{{citazionenecessaria}}')
    tmp_to_clarify = t.count('{{chiarire') + t.count('{{chiarire}}')

    return str(sum_of_warnings), str(tmp_without_sources), str(tmp_to_clarify)


# Function to find template
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
def analysis(language, discussionURL, first_edit, dimension, immages, note, featured, 
             warnings_config, discussion_size, views, incipit_size, common_gallery,
             common_pages, itwikisource,wikiversity, wikibooks, quality, review, biblography, coordinate):
   f = open('query.csv', "r")
   lines = f.readlines()   
    
   #delete the contents of the file before starting
   results = open('resultati.txt',"w")
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

        result = ris + line +"\t" +"Voce inesistente"

       

      else:

        if first_edit:
           result = result + first_edit(line2) + "\t"

        if dimension:
           result = result + dimension(wikitext) + "\t"

        if immages:
           result = result + immages(wikitext) + "\t"

        if note:
           result = result + note(wikitext) + "\t"

        if warnings_config:
           for i in count_warnings(wikitext):
              print("some avisi")
              ris = ris + i + "\t"   

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

              ris = ris + wikidata["entities"][wikidataid]["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]["latitude"] + "\t"

              ris = ris + wikidata["entities"][wikidataid]["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]["longitude"] + "\t"

           except:

              ris = ris + "\t" + "\t"

      results.write(result + "\n")  # aggiungere un salto di linea dopo ogni risultato
      results.close()  # chiudere il file
      print (result)



# Function to get configuration based on the Wikipedia language
def get_wikipedia_config(language):
    return wikipedia_config.get(language, {})   

def main():
    # Specify the Wikipedia language
    wikipedia_language = "es"  # Change this to the desired Wikipedia language

    # Get the Wikipedia-specific configuration
    wikipedia_specific_config = get_wikipedia_config(wikipedia_language)

    # Access configuration variables based on the language
    language = wikipedia_specific_config.get("language")

    dimension_option = wikipedia_specific_config.get("dimension")
    first_edit_option = wikipedia_specific_config.get("first_edit") 
    note_option = wikipedia_specific_config.get("note")
    images_option = wikipedia_specific_config.get("images")
    views_option = wikipedia_specific_config.get("views")
    incipit_size_option = wikipedia_specific_config.get("incipit_size")
    discussion_size_option = wikipedia_specific_config.get("discussion_size")
    discussionURL = wikipedia_specific_config.get("discussionURL")
    wikidata_option = wikipedia_specific_config("wikidata")
    
    warnings_config = wikipedia_specific_config.get("warnings_config")
    common_pages_option = wikipedia_specific_config.get("common_pages")
    common_gallery_option = wikipedia_specific_config.get("common_gallery")
    itwikisource_option = wikipedia_specific_config.get("itwikisource")
    wikiversity_option = wikipedia_specific_config.get("wikiversity")
    wikibooks_option = wikipedia_specific_config.get("wikibooks")
    feature_option = wikipedia_language("featured")
    quality_option = wikipedia_specific_config.get("quality")
    review_option = wikipedia_specific_config.get("review")
    bibliography_option = wikipedia_specific_config.get("bibliography")
    coordinate_option = wikipedia_specific_config.get("coordinate")
    featured_template = wikipedia_specific_config.get("featured_template")
    dispay_window_template = wikipedia_specific_config.get("dispay_window_template")

    # Call your analysis function or other code logic here, passing the parameters
    analysis(
        language=language,
        discussionURL=discussionURL,
        first_edit=first_edit_option,
        dimension=dimension_option,
        images=images_option,
        note=note_option,
        featured=quality_option, 
        warnings_config=warnings_config,
        discussion_size=discussion_size_option,
        views=views_option,
        incipit_size=incipit_size_option,
        common_gallery=common_gallery_option,
        common_pages=common_pages_option,
        itwikisource=itwikisource_option,
        wikiversity=wikiversity_option,
        wikibooks=wikibooks_option,
        quality=quality_option,
        review=review_option,
        bibliography=bibliography_option,
        coordinate=coordinate_option,
        featured_template=featured_template,
        dispay_window_template=dispay_window_template,
    )

if __name__ == "__main__":
    main()
