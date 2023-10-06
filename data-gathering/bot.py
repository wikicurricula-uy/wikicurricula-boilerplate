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


#language subdomain, to be used for API calls
language = "es"

idwikidata = 1

dimension = 1

firstEdit = 1

note         =  1

images  = 1

display = 1

dimensionIncipit  = 1

discussionDimension = 1

#discussion page prefix
discussion = "Discusión:"
discussionURL = urllib.parse.quote(discussion)

#currently, the notice count does not work for the Spanish Wikipedia
configAlerts = 0

commonsPage = 1

commonsGallery = 1

itwikisource = 1

wikiversity = 1

wikibooks = 1

showcase = 1

#template display
showcaseTemplate ="{{featured article"

quality = 1

#"Quality article template

qualityArticleTemplate="{{good article"

review = 1

bibliography = 1

coordinates = 1

# function fetches the pageviews of an article within a given date range and then calculates the average daily pageviews for that period.
# Returns either the calculated average daily pageviews as a string or "ERROR" if an exception occurs.

def get_avg_pageviews(article, start, end):

   #params: article: article title, start: start date of the period, end: end date of the period
   SUM = 0

   try:

      #  query the Wikimedia REST API for pageviews data.
      url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"+language+".wikipedia/all-access/user/"+article+"/daily/"+start+"/"+end
   
      html = urlopen(url).read()



      html = str(html)

      html = html.replace('{"items":[',"")

      html = html.replace(']}',"")

      n = html.count("}")


      # Calculate the sum of daily pageviews
      for i in range(n):

         txt = html[:html.find("}")+1]

         SUM += int(txt[txt.find('"views":')+len('"views":'):-1])

         html =html.replace(txt,"",1)

      # Determine the number of days in the specified date range.
      d1 = datetime.strptime(start, "%Y%m%d")
      d2 = datetime.strptime(end, "%Y%m%d")
      days = (abs((d2 - d1).days)+1)
      
      # average daily pageviews is sum divided number of days
      ris = str(int(round((SUM/days),0)))

      # If an error occurs (e.g., network issues or problems with the API call), catch the exception and set ris to the string "ERROR
   except:

      ris = "ERROR"
   return ris


# returns visits since the beginning of time, average daily visits since the begininning of time, average daily visits in the specified year
def visits(article):

  #YYYYMMGG
  START_ALL_TIME = "20150701"; 

  START_PREV_YEAR = "20220101";
  END_PREV_YEAR = "20221231";

  START_CURRENT_YEAR = "20230101";
  END_CURRENT_YEAR   = "20230831";  

  DATE = []


  #calculate ris1, total pageviews since the beginning of time, and ris2, average pageviews since de beginning of time
  d1 = datetime.strptime(START_ALL_TIME, "%Y%m%d")

  d2 = datetime.strptime(END_CURRENT_YEAR, "%Y%m%d")

  days = (abs((d2 - d1).days)+1)

  article = article.replace(" ","_")

  SUM = 0

  try:

    url ="https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"+lingua+".wikipedia/all-access/user/"+article+"/daily/"+START_ALL_TIME +"/" + END_CURRENT_YEAR

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



      ris1 = str(SUM)

      ris2 = str(int(round((SUM/days),0)))

  except:

    ris1 = "ERROR"

    ris2 = "ERROR"

  #calculate ris3, average pageviews from previous year
  ris3 = get_avg_pageviews(article, START_PREV_YEAR, END_PREV_YEAR)

  #calculate ris4, average pageviews from current year
  ris4 = get_avg_pageviews(article, START_CURRENT_YEAR, END_CURRENT_YEAR)

   
  return str(ris1), str(ris2), str(ris3), str(ris4)




# return the id of an item.
def name2Q(item):

  return item.getID()




# count the number of times '</ref>' appears in a given text and then return the count as a string.
def note(text):

  return str(text.count('</ref>'))




# determine the length of a text and then return it as a string.
def dimension(text):
  return str(len(text))




# calculates the sum of occurrences of various image file extensions in the lowercase text and then returns the sum as a string.
def images(text):

  t = text.lower()

  img = str(t.count('.jpg')+t.count('.svg')+t.count('.jpeg')+t.count('.png')+t.count('.tiff')+t.count('.gif')+t.count('.tif')+t.count('.xcf'))

  return img




# retrieve the date of the first edit made to a specified article.
def firstEdit(article):

  try:

   # query the XTools API for information about the specified article.
    url ="https://xtools.wmflabs.org/api/page/articleinfo/"+language+".wikipedia.org/"+article.replace(" ","_")
    # 
    html = urlopen(url).read()

    html = str(html)

   # extract the creation date of the article and extract the subsequent characters.

    html = html[html.find("created_at")+len("created_at")+3:]

    html = html[:10]

# Incase of an error (e.g., a network issue, or the article is not found), the code within this block will execute
  except:

    html= "ERROR"

  return html




# The function counts the occurrences of different types of tags and returns the counts.
def alerts(t):

# A temporary copy of the original text is created
   t_tmp = t

   t = t.replace("\n","")

   t = t.replace(" ","")

   t = t.lower()

    
   #  count the occurrences of various templates or tags related to potential issues or improvement areas
   tmpCheck = t.count('{{c|') + t.count('{{c}}')

   tmpSummary = t.count('{{tmp|')  + t.count('{{tmp}}')

   tmpHelp = t.count('{{a|')

   tmpCorrect = t.count('{{correct')

   tmpCuriosity = t.count('{{curiosity')

   tmpDivide = t.count('{{d|') + t.count('{{d}')

   tmpSources = t.count('{{f|')  + t.count('{{f}}')

   tmpLocalism = t.count('{{l|')  + t.count('{{l}}')

   tmpPOV = t.count('{{p|')  + t.count('{{p}}')

   tmpNN = t.count('{{nn|')  + t.count('{{nn}}')

   tmpRecentism = t.count('{{recentism')

   tmpManual = t.count('{{manualstyle')

   tmpTranslation = t.count('{{t|')  + t.count('{{t}}')

   tmpWikify = t.count('{{w|')  + t.count('{{w}}')

   tmpStub = t.count('{{s|')  + t.count('{{s}}')

   tmpsectionStub = t.count('{{sectionstub')

   tmpControlCopi = t.count('{{controlcopy')



   sumAlerts = tmpCheck + tmpSummary + tmpHelp + tmpCorrect + tmpCuriosity + tmpDivide + tmpSources + tmpLocalism + tmpPOV

   sumAlerts = sumAlerts + tmpNN + tmpRecentism + tmpManual + tmpTranslation + tmpWikify + tmpStub + tmpsectionStub + tmpControlCopi



   tmpWithoutSources= t.count('{{withoutsource') + t.count('{{citationrequired') + t.count('{{withoutsource}}') + t.count('{{citationrequired}}')

   tmpClarify = t.count('{{clarify') + t.count('{{clarify}}')


   # return the total count of alerts, the count of instances without sources, and the count of instances needing clarification
   return str(sumAlerts), str(tmpWithoutSources), str(tmpClarify)




# extract a specific template from a given text. returns either the modified text (if a template is found) or the original text
def findtemplate(text):

      #  copies of the input text with the first two characters removed.
      tmp = text[2:]

      tmp2 = text[2:]

      # include only the portion of text from the beginning to the first occurrence of "}}" plus two characters.
      tmp = tmp[:tmp.find("}}")+2]

      if "{{" in tmp:

         # substring of tmp starting from the first occurrence of "{{" to the end.
          tmp3 = tmp[tmp.find("{{"):]

         # replace tmp3 with a placeholder string 
          tmp2 = tmp2.replace(tmp3,"$$$$$$$$$$$$$$")


         # include only the portion up to the first occurrence of "}}" plus two characters

          tmp2 = tmp2[:tmp2.find("}}")+2]
         
         # placeholder is replaced back with the original template (tmp3)
          tmp2 = tmp2.replace("$$$$$$$$$$$$$$",tmp3)

          return tmp2

      return tmp




# calculate the length of an introductory part of a text while handling various text manipulations.
def lengthIncipit(text):

   incipit = text

   #  extract the part of the text up to the first occurrence of "\n==" using incipit = incipit[:incipit.find("\n==")].

   incipit = incipit[:incipit.find("\n==")]

   ntemplate  = incipit.count('{{')

   incipitclear = incipit

   # Handling '{{formatnum:' Templates:
   fn = incipit.count("{{formatnum:")

   for i in range(fn):

      tmp = incipit[incipit.find("{{formatnum:"):]

      tmp = tmp[:tmp.find("}}")+2]

      tmp2 = tmp.replace("{{formatnum:","")

      tmp2 = tmp2.replace("}}","")

      incipit = incipit.replace(tmp, tmp2)


   # Handling Other '{{' Templates:
   ntemplate = incipit.count("{{")

   for i in range(ntemplate):

      text = incipit[incipit.find("{{"):]

      template = findtemplate(text)

      text = text.replace("{{"+template,"")

      incipit = incipit.replace("{{"+template,"")

   # Removing '<ref>' Tags
   incipit = incipit.replace("</ref>","")

   n = incipit.count("<ref")

   # Removing '[[' and ']]' Tags, and '|':
   for i in range(n):

      tmp = incipit[incipit.find("<ref"):]

      tmp = tmp[:tmp.find(">")+1]

      incipit = incipit.replace(tmp,"")

   incipit = incipit.replace("[[","")

   incipit = incipit.replace("]]","")

   incipit = incipit.replace("|","")

   # Calculating Length:
   lunincipit = len(incipit)
   return str(lunincipit)




#  check whether "qualityArticleTemplate" is present in the provided text
def qualityArticle(text):

   if qualityArticleTemplate in text.lower():

      return "1"

   else:

      return "0"


# check whether "showcaseTemplate" is present in the provided text
def showcase(text):

   if showcaseTemplate in text.lower():

      return "1"

   else:

      return "0"





    
# analyze articles
def analysis():
   f = open('query.csv', "r")

   vox = f.readlines()   
    
   # delete the contents of the file before starting
   
   results = open('results.txt',"w")
   
   results.truncate(0)
   
   results.close()

   for article in vox:
      
      
      results = open('results.txt', 'a')  # open the file in append mode

      flag = 1

      article = article[:-1]

      article = article.replace(" ","_")

      ris = ""

      wikitext = ""



      article2 = urllib.parse.quote(article)

      article = article.replace(" ","_")


      try:

        url = "https://"+language+".wikipedia.org/w/api.php?action=parse&page=" + article2 + "&prop=wikitext&formatversion=2&format=json"

        json_url = urlopen(url)

        data = json.loads(json_url.read())

        wikitext = data["parse"]["wikitext"]

        if "#REDIRECT"  in wikitext:

     #   print (wikitext)

          article2 = wikitext[wikitext.find("[[")+2:]

          article2 = article2[:article2.find("]]")]

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



        ris = ris + article + "\t"

        ris = ris + wikidataid + "\t"

      except:

        ris = ris + article +"\t" +"non-existent article"

       

      else:

        if firstEdit:

           ris = ris + firstEdit(article2) + "\t"



        if dimension:

           ris = ris + dimension(wikitext) + "\t"



        if images:

           ris = ris + images(wikitext) + "\t"



        if note:

           ris = ris + note(wikitext) + "\t"

           

        if configAlerts:

           for i in alerts(wikitext):
              print("some avisi")
              ris = ris + i + "\t"

               

        if discussionDimension:

           ris = ris + dimension(wikitext_discussion) + "\t"



        if dimensionIncipit:

           ris = ris + lengthIncipit(wikitext) + "\t"

           

        if visits:

         for i in visits(article2):

              ris = ris + i + "\t"



        if qualityArticle:

           ris = ris + qualityArticle(wikitext) + "\t"



        if showcase:

           ris = ris + showcase(wikitext) + "\t"



        if commonsGallery:

           try:

              ris = ris + wikidata["entities"][wikidataid]["claims"]["P373"][0]["mainsnak"]["datavalue"]["value"] + "\t"

           except:

              ris = ris + "" + "\t"



        if  commonsPage:

           try:

              ris = ris + wikidata["entities"][wikidataid]["claims"]["P935"][0]["mainsnak"]["datavalue"]["value"] + "\t"

           except:

              ris = ris + "" + "\t"

   

        if itwikisource:

           try:

              ris = ris + wikidata["entities"][wikidataid]["sitelinks"]["itwikisource"]["title"] + "\t"

           except:

              ris = ris + "\t"



        if coordinates:

           try:

              ris = ris + wikidata["entities"][wikidataid]["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]["latitude"] + "\t"

              ris = ris + wikidata["entities"][wikidataid]["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]["longitude"] + "\t"

           except:

              ris = ris + "\t" + "\t"

      
      results.write(ris + "\n")  # add a line break after each result
      
      results.close()  # close the file
      print (ris)

     

def main():

   analysis()



if __name__ == "__main__":

   main()