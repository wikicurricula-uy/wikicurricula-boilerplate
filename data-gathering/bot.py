'''
Python script for performing various analyses on Wikipedia articles. 
This script appears to collect data from Wikipedia and Wikidata, 
process it, and save the results to a file. 
'''

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


# subdomain of language, to be used for API calls
language = "en"

id_wikidata= 1

dimension = 1

first_edit = 1

note  =  1

images  = 1

views = 1

incipit_size = 1

discussion_size = 1

# discussion prefix
discussion = "Discusión:"
discussionURL = urllib.parse.quote(discussion)


warnings_config = 0

common_pages = 1

common_gallery = 1

itwikisource = 1

wikiversity = 1

wikibooks = 1

featured = 1

featured_template="{{artículo destacado" # featured template

quality = 1

template_quality="{{artículo bueno" # quality of template

review= 1

bibliography = 1

coordinate = 1

# Function to get average page views: returns visits since the beginning of time, average dayly visits since the begininning of time, average daily visits in the specified year
def get_avg_pageviews(article_title, start, end):
   SUM = 0

   try:

      url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"+language+".wikipedia/all-access/user/"+article_title+"/daily/"+start+"/"+end
      
      html = urlopen(url).read()

      html = str(html)

      html = html.replace('{"items":[',"")

      html = html.replace(']}',"")

      n = html.count("}")


      for i in range(n):

         txt = html[:html.find("}")+1]

         SUM += int(txt[txt.find('"views":')+len('"views":'):-1])

         html =html.replace(txt,"",1)
      
      d1 = datetime.strptime(start, "%Y%m%d")
      d2 = datetime.strptime(end, "%Y%m%d")
      days = (abs((d2 - d1).days)+1)
      result = str(int(round((SUM/days),0)))

   except:

      result = "ERROR"
   
   return result

# returns visits since the beginning of time, average dayly visits since the begininning of time, average daily visits in the specified year
def visit(article):

   #YYYYMMGG
   START_ALL_TIME = "20150701"; 

   START_PREV_YEAR = "20220101"; 
   END_PREV_YEAR = "20221231"; 

   START_CURRENT_YEAR = "20230101"; 
   END_CURRENT_YEAR   = "20230831"; 

   DATE = []


   #calculate result1, total pageviews since the beginning of time, and result2, average pageviews since de beginning of time
   d1 = datetime.strptime(START_ALL_TIME, "%Y%m%d")

   d2 = datetime.strptime(END_CURRENT_YEAR, "%Y%m%d")

   days = (abs((d2 - d1).days)+1)

   ARTICLE = article.replace(" ","_")

   SUM = 0

   try:

      url ="https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"+language+".wikipedia/all-access/user/"+ARTICLE+"/daily/"+START_ALL_TIME +"/" + END_CURRENT_YEAR

      html = urlopen(url).read()

      ecc = 0 # to change

      if ecc == 0:

         html = str(html)

         html = html.replace('{"items":[',"")

         html = html.replace(']}',"")

         n = html.count("}")



         for i in range(n):

            txt = html[:html.find("}")+1]

            SUM += int(txt[txt.find('"views":')+len('"views":'):-1])

            html =html.replace(txt,"",1)



         result1 = str(SUM)

         result2 = str(int(round((SUM/days),0)))

   except:

      result1 = "ERROR"

      result2 = "ERROR"

   #calculate result3, average pageviews from previous year
   result3 = get_avg_pageviews(article, START_PREV_YEAR, END_PREV_YEAR)

   #calculate result4, average pageviews from current year
   result4 = get_avg_pageviews(article, START_CURRENT_YEAR, END_CURRENT_YEAR)

      
   return str(result1), str(result2), str(result3), str(result4)




# Function to return ID of an item
def nome2Q(item):
   return item.getID()




#This function counts the number of times the substring "</ref>" appears within the input string "text" and converts the count (which is an integer) into a string
def note(text):
   return str(text.count('</ref>'))



# Function to calculate and return the length of a given string as a string.
def dimension(text):
    return str(len(text))



# this function counts the occurrences of specific image file extensions within a given string and returns that count as a string.
def images(text):

   t = text.lower()

   img = str(t.count('.jpg')+t.count('.svg')+t.count('.jpeg')+t.count('.png')+t.count('.tiff')+t.count('.gif')+t.count('.tif')+t.count('.xcf'))

   return img




'''This function relies on external web scraping 
it reads the HTML content of the page and converts it's content to a string and then extracts a specific portion of the HTML using string manipulation. 
Specifically, it looks for the substring "created_at" and extracts the following 10 characters, which should represent the creation date of the Wikipedia article.'''

def first_edit(article):
   try:

      url ="https://xtools.wmflabs.org/api/page/articleinfo/"+language+".wikipedia.org/"+article.replace(" ","_")
      html = urlopen(url).read()

      html = str(html)

      html = html[html.find("created_at")+len("created_at")+3:]

      html = html[:10]

   except:

      html= "ERROR"

   return html




# This function analyzes and count specific types of tags within a given text. The results are returned as strings, making them suitable for further processing.
def warnings(t):

   t_tmp =t
   t = t.replace("\n","")
   t = t.replace(" ","")
   t = t.lower()

    
   tmp_to_check = t.count('{{c|') + t.count('{{c}}')

   tmp_synoptic = t.count('{{tmp|')  + t.count('{{tmp}}')

   tmp_help = t.count('{{a|')

   tmp_correct = t.count('correggere{{')

   tmp_curiosity = t.count('{{curiosit')

   tmp_divide = t.count('{{d|') + t.count('{{d}')

   tmp_sources = t.count('{{f|')  + t.count('{{f}}')

   tmp_localism = t.count('{{l|')  + t.count('{{l}}')

   tmp_pov = t.count('{{p|')  + t.count('{{p}}')

   tmp_nn= t.count('{{nn|')  + t.count('{{nn}}')

   tmp_recentism = t.count('{{recentismo')

   tmp_manual_style = t.count('{{stilemanualistico')

   tmp_translation = t.count('{{t|')  + t.count('{{t}}')

   tmp_wikificare = t.count('{{w|')  + t.count('{{w}}')

   tmp_stub = t.count('{{s|')  + t.count('{{s}}')

   tmp_stub_section = t.count('{{stubsezione')

   tmp_copy_control = t.count('{{controlcopy')



   sum_of_warnings = tmp_to_check + tmp_synoptic + tmp_help + tmp_correct + tmp_curiosity + tmp_divide + tmp_sources + tmp_localism + tmp_pov
   sum_of_warnings += tmp_nn + tmp_recentism + tmp_manual_style + tmp_translation + tmp_wikificare + tmp_stub + tmp_stub_section + tmp_copy_control



   tmp_without_sources = t.count('{{senzafonte') + t.count('{{citazionenecessaria') + t.count('{{senzafonte}}') + t.count('{{citazionenecessaria}}')

   tmp_to_clarify = t.count('{{chiarire') + t.count('{{chiarire}}')



   return str(sum_of_warnings), str(tmp_without_sources), str(tmp_to_clarify)




# This function is designed to iteratively find and extract templates from a text until no more templates are present
def find_template(text):

   tmp = text[2:]
   tmp2 = text[2:]
   tmp = tmp[:tmp.find("}}")+2]

   if "{{" in tmp:

      tmp3 = tmp[tmp.find("{{"):]
      tmp2 = tmp2.replace(tmp3,"$$$$$$$$$$$$$$")


      tmp2 = tmp2[:tmp2.find("}}")+2]
      tmp2 = tmp2.replace("$$$$$$$$$$$$$$",tmp3)

      return tmp2
   return tmp




# Function to calculate the length of the introduction
#Incipit means the opening of a manuscript, early printed book. Hence, incipit == introduction 
def calculate_introduction_length(text):

   incipit = text

   incipit = incipit[:incipit.find("\n==")]

   template_count  =incipit.count('{{')

   # incipitclear = incipit

   format_num = incipit.count("{{formatnum:")

   for i in range(format_num):

      tmp = incipit[incipit.find("{{formatnum:"):]

      tmp = tmp[:tmp.find("}}")+2]

      tmp2 = tmp.replace("{{formatnum:","")

      tmp2 = tmp2.replace("}}","")

      incipit = incipit.replace(tmp, tmp2)



   template_count = incipit.count("{{")

   for i in range(template_count):

      text = incipit[incipit.find("{{"):]

      template = find_template(text)

      text = text.replace("{{"+template,"")

      incipit = incipit.replace("{{"+template,"")

   incipit = incipit.replace("</ref>","")

   n = incipit.count("<ref")

   for i in range(n):

      tmp = incipit[incipit.find("<ref"):]

      tmp = tmp[:tmp.find(">")+1]

      incipit = incipit.replace(tmp,"")

   incipit = incipit.replace("[[","")

   incipit = incipit.replace("]]","")

   incipit = incipit.replace("|","")

   introduction_length = len(incipit)
   return str(introduction_length)




# Function to check if the article is a "good article"
def vdq(text):
   if template_quality in text.lower():
      return "1"

   else:
      return "0"


# This function checks to if a specific template (defined by the vdqTemplate variable) is present in the provided text.
def featured_in(text):
   if featured_template in text.lower():
      return "1"

   else:
      return "0"


    
# Main analysis function
def analysis():
   # f = open('query.csv', "r") #Adding a character encoding will required for some characters in the query.csv file to avoid getting a UnicodeDecodeError
   f = open('query.csv', 'r')

   articles = f.readlines()   
    
   # delete the contents of the file before starting
   results = open('results.txt',"w")
   results.truncate(0)
   results.close()

   for article in articles:
      results = open('results.txt', 'a')  # open the file in append mode

      flag = 1

      article = article[:-1]
      article= article.replace(" ","_")
      result = ""
      wikitext = ""

      article2 = urllib.parse.quote(article)
      article = article.replace(" ","_")


      try:

         url = "https://"+language+".wikipedia.org/w/api.php?action=parse&page=" + article2 + "&prop=wikitext&formatversion=2&format=json"
         json_url = urlopen(url)

         data = json.loads(json_url.read())

         wikitext = data["parse"]["wikitext"]

         if "#RINVIA"  in wikitext:
         #   print (wikitext)

            article2 = wikitext[wikitext.find("[[")+2:]
            article2 = article2[:article.find("]]")]
            article = article2
            article2 = article2.replace("_"," ")

      except:
         pass                                     

      try:

         article2 = urllib.parse.quote(article)

         article = article.replace(" ","_")

         url = "https://"+language+".wikipedia.org/w/api.php?action=query&titles=" + article2 +"&prop=pageprops&format=json&formatversion=2"

         json_url = urlopen(url)

         data = json.loads(json_url.read())

         wikidataid = data["query"]["pages"][0]["pageprops"]["wikibase_item"]

         url ="https://www.wikidata.org/wiki/Special:EntityData/"+wikidataid+".json"

         json_url = urlopen(url)

         wikidata = json.loads(json_url.read())



         url = "https://"+language+".wikipedia.org/w/api.php?action=parse&page=" + article2 + "&prop=wikitext&formatversion=2&format=json"

         json_url = urlopen(url)

         data = json.loads(json_url.read())

         wikitext = data["parse"]["wikitext"]



         try:

            url = "https://"+language+".wikipedia.org/w/api.php?action=parse&page=" + discussionURL + article2 + "&prop=wikitext&formatversion=2&format=json"
            json_url = urlopen(url)

            data = json.loads(json_url.read())

            wikitext_discussion = data["parse"]["wikitext"]

         except:
            wikitext_discussion = ""

         result = result + article + "\t"

         result = result + wikidataid + "\t"

      except:
         result = result + article +"\t" +"voice non-existent"

       

      else:

         if first_edit:
            result = result + first_edit(article2) + "\t"

         if dimension:
            result = result + dimension(wikitext) + "\t"

         if images:
            result = result + images(wikitext) + "\t"

         if note:
            result = result + note(wikitext) + "\t"

           

         if warnings_config:
            for i in warnings(wikitext):
               print("some warnings")
               result = result + i + "\t"   

         if discussion_size:
            result = result + dimension(wikitext_discussion) + "\t"

         if incipit_size:
            result = result + calculate_introduction_length(wikitext) + "\t"


         if visit:
            for i in visit(article2):
               result = result + i + "\t"

         if vdq:
            result = result + vdq(wikitext) + "\t"



         if featured:
            result = result + featured_in(wikitext) + "\t"



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

      results.write(result + "\n")  # add a line break after each result
      results.close()  # close the file
      print (result)

     

def main():
   analysis()



if __name__ == "__main__":
   main()