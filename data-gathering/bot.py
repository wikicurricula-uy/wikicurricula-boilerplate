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

visualization = 1

dimensionIncipit = 1

sizeDiscussion = 1
#discussion page prefix
discussion = "Discussion:"
discussionURL = urllib.parse.quote(discussion)

#At the moment, the notice count does not work for Wikipedia in Spanish
configNotices = 0

commonPages = 1

commonGallery = 1

itwikisource = 1

wikiversita = 1

wikibooks = 1

window = 1
#window template
windowTemplate="{{featured article"

quality = 1
#quality entry template
vdqTemplate="{{good article"

sifter = 1

bibliography = 1

coordinate = 1


def get_avg_pageviews(voice, start, end):
  SOMMA = 0;

  try:

    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"+language+".wikipedia/all-access/user/"+voice+"/daily/"+start+"/"+end
   
    html = urlopen(url).read()



    html = str(html);

    html = html.replace('{"items":[',"")

    html = html.replace(']}',"")

    n = html.count("}")



    for i in range(n):

       txt = html[:html.find("}")+1]

       SOMMA += int(txt[txt.find('"views":')+len('"views":'):-1])

       html =html.replace(txt,"",1)
    
    d1 = datetime.strptime(start, "%Y%m%d")
    d2 = datetime.strptime(end, "%Y%m%d")
    days = (abs((d2 - d1).days)+1)
    res = str(int(round((SOMMA/days),0)))

  except:

    res = "ERRORE"
  
  return res

# returns visits since the beginning of time, average dayly visits since the begininning of time, average daily visits in the specified year
def visits(voice):

  #YYYYMMGG
  START_ALL_TIME = "20150701"; 

  START_PREV_YEAR = "20220101";
  END_PREV_YEAR = "20221231";

  START_CURRENT_YEAR = "20230101";
  END_CURRENT_YEAR   = "20230831";  

  DATE = []


  #calculate res1, total pageviews since the beginning of time, and res2, average pageviews since de beginning of time
  d1 = datetime.strptime(START_ALL_TIME, "%Y%m%d")

  d2 = datetime.strptime(END_CURRENT_YEAR, "%Y%m%d")

  days = (abs((d2 - d1).days)+1)

  VOICE = voice.replace(" ","_")

  SUM = 0

  try:

    url ="https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"+language+".wikipedia/all-access/user/"+VOICE+"/daily/"+START_ALL_TIME +"/" + END_CURRENT_YEAR

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



      res1 = str(SUM)

      res2 = str(int(round((SUM/days),0)))

  except:

    res1 = "ERRORE"

    res2 = "ERRORE"

  #calculate res3, average pageviews from previous year
  res3 = get_avg_pageviews(VOCE, START_PREV_YEAR, END_PREV_YEAR)

  #calculate res4, average pageviews from current year
  res4 = get_avg_pageviews(VOCE, START_CURRENT_YEAR, END_CURRENT_YEAR)

   
  return str(res1), str(res2), str(res3), str(res4)





def name2Q(item):

  return item.getID()





def note(text):

  return str(text.count('</ref>'))





def dimension(text):
  return str(len(text))





def images(text):

  t = text.lower()

  img = str(t.count('.jpg')+t.count('.svg')+t.count('.jpeg')+t.count('.png')+t.count('.tiff')+t.count('.gif')+t.count('.tif')+t.count('.xcf'))

  return img





def firstEdit(voice):

  try:

    url ="https://xtools.wmflabs.org/api/page/articleinfo/"+language+".wikipedia.org/"+voice.replace(" ","_")
    html = urlopen(url).read()

    html = str(html)

    html = html[html.find("created_at")+len("created_at")+3:]

    html = html[:10]

  except:

    html= "ERRORE"

  return html





def alerts(t):

   t_tmp =t

   t = t.replace("\n","")

   t = t.replace(" ","")

   t = t.lower()

    

   tmpcheck = t.count('{{c|') + t.count('{{c}}')

   tmpsynoptic = t.count('{{tmp|')  + t.count('{{tmp}}')

   tmphelp = t.count('{{a|')

   tmpcorrect = t.count('{{correct')

   tmpcuriosity = t.count('{{curiosit')

   tmpshare = t.count('{{d|') + t.count('{{d}')

   tmpsources = t.count('{{f|')  + t.count('{{f}}')

   tmplocalism = t.count('{{l|')  + t.count('{{l}}')

   tmpPOV = t.count('{{p|')  + t.count('{{p}}')

   tmpNN = t.count('{{nn|')  + t.count('{{nn}}')

   tmprecentism = t.count('{{recentism')

   tmpmanual = t.count('{{manualstyle')

   tmptranslation = t.count('{{t|')  + t.count('{{t}}')

   tmpwikificare = t.count('{{w|')  + t.count('{{w}}')

   tmpstub = t.count('{{s|')  + t.count('{{s}}')

   tmpstubsection = t.count('{{stubsection')

   tmpcontrolcopy = t.count('{{controlcopy')



   sumalerts = tmpcheck + tmpsynoptic + tmphelp + tmpcorrect + tmpcuriosity + tmpshare + tmpsources + tmplocalism + tmpPOV

   sumalerts = sumalerts + tmpNN + tmprecentism + tmpmanual + tmptranslation + tmpwikificare + tmpstub + tmpstubsection + tmpcontrolcopy



   tmpwithoutsources = t.count('{{withoutsource') + t.count('{{citationrequired') + t.count('{{withoutsource}}') + t.count('{{citationrequired}}')

   tmpclarify = t.count('{{clarify') + t.count('{{clarify}}')



   return str(sumalerts), str(tmpwithoutsources), str(tmpclarify)





def findtemplate(text):

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





def lengthIncipit(text):

   incipit = text

   incipit = incipit[:incipit.find("\n==")]

   ntemplate  =incipit.count('{{')

   incipitclear = incipit

   fn = incipit.count("{{formatnum:")

   for i in range(fn):

      tmp = incipit[incipit.find("{{formatnum:"):]

      tmp = tmp[:tmp.find("}}")+2]

      tmp2 = tmp.replace("{{formatnum:","")

      tmp2 = tmp2.replace("}}","")

      incipit = incipit.replace(tmp, tmp2)



   ntemplate = incipit.count("{{")

   for i in range(ntemplate):

      text = incipit[incipit.find("{{"):]

      template = findtemplate(text)

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

   lunincipit = len(incipit)
   return str(lunincipit)





def vdq(text):

   if vdqTemplate in text.lower():

      return "1"

   else:

      return "0"



def window(text):

   if windowTemplate in text.lower():

      return "1"

   else:

      return "0"





    

def analysis():
   f = open('query.csv', "r")

   vox = f.readlines()   
    
   # delete the content of the file before starting
   results = open('results.txt',"w")
   results.truncate(0)
   results.close()

   for voice in vox:
      
      results = open('results.txt', 'a')  # open the file in append mode

      flag = 1

      voice = voice[:-1]

      voice = voice.replace(" ","_")

      res = ""

      wikitext = ""



      voice2 = urllib.parse.quote(voice)

      voice = voice.replace(" ","_")


      try:

        url = "https://"+language+".wikipedia.org/w/api.php?action=parse&page=" + voice2 + "&prop=wikitext&formatversion=2&format=json"

        json_url = urlopen(url)

        data = json.loads(json_url.read())

        wikitext = data["parse"]["wikitext"]

        if "#RINVIA"  in wikitext:

     #   print (wikitext)

          voice2 = wikitext[wikitext.find("[[")+2:]

          voice2 = voice2[:voice2.find("]]")]

          voice = voice2

          voice2 = voice2.replace("_"," ")

      except:

        pass                                     

      try:

        voice2 = urllib.parse.quote(voice)

        voice = voice.replace(" ","_")

        url = "https://"+language+".wikipedia.org/w/api.php?action=query&titles=" + voice2 +"&prop=pageprops&format=json&formatversion=2"

        json_url = urlopen(url)

        data = json.loads(json_url.read())

        wikidataid = data["query"]["pages"][0]["pageprops"]["wikibase_item"]

        url ="https://www.wikidata.org/wiki/Special:EntityData/"+wikidataid+".json"

        json_url = urlopen(url)

        wikidata = json.loads(json_url.read())



        url = "https://"+language+".wikipedia.org/w/api.php?action=parse&page=" + voice2 + "&prop=wikitext&formatversion=2&format=json"

        json_url = urlopen(url)

        data = json.loads(json_url.read())

        wikitext = data["parse"]["wikitext"]



        try:

          url = "https://"+language+".wikipedia.org/w/api.php?action=parse&page=" + discussionURL + voice2 + "&prop=wikitext&formatversion=2&format=json"
          json_url = urlopen(url)

          data = json.loads(json_url.read())

          wikitext_discussion = data["parse"]["wikitext"]

        except:

          wikitext_discussion = ""



        res = res + voice + "\t"

        res = res + wikidataid + "\t"

      except:

        res = res + voice +"\t" +"Voice inexistent"

       

      else:

        if firstEdit:

           res = res + firstEdit(voice2) + "\t"



        if dimension:

           res = res + dimension(wikitext) + "\t"



        if images:

           res = res + images(wikitext) + "\t"



        if note:

           res = res + note(wikitext) + "\t"

           

        if configAlerts:

           for i in alerts(wikitext):
              print("some alerts")
              res = res + i + "\t"

               

        if dimensiondiscussion:

           res = res + dimension(wikitext_discussion) + "\t"



        if dimensionIncipit:

           res = res + lengthIncipit(wikitext) + "\t"

           

        if visits:

           for i in visits(voice2):

              res = res + i + "\t"



        if vdq:

           res = res + vdq(wikitext) + "\t"



        if window:

           res = res + window(wikitext) + "\t"



        if commonGallery:

           try:

              res = res + wikidata["entities"][wikidataid]["claims"]["P373"][0]["mainsnak"]["datavalue"]["value"] + "\t"

           except:

              res = res + "" + "\t"



        if commonPages:

           try:

              res = res + wikidata["entities"][wikidataid]["claims"]["P935"][0]["mainsnak"]["datavalue"]["value"] + "\t"

           except:

              res = res + "" + "\t"

   

        if itwikisource:

           try:

              res = res + wikidata["entities"][wikidataid]["sitelinks"]["itwikisource"]["title"] + "\t"

           except:

              res = res + "\t"



        if coordinate:

           try:

              res = res + wikidata["entities"][wikidataid]["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]["latitude"] + "\t"

              res = res + wikidata["entities"][wikidataid]["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]["longitude"] + "\t"

           except:

              res = res + "\t" + "\t"

      results.write(res + "\n")  # add a line break after each result
      results.close()  # close the file
      print (res)

     

def main():

   analysis()



if __name__ == "__main__":

   main()