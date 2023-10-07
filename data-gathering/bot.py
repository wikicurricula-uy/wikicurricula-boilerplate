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

primoEdit = 1

note         =  1

images  = 1

views = 1

dimensionStart = 1

dimensionDiscussion = 1
#prefisso della pages di discussion
discussion = "Discusión:"
discussionURL = urllib.parse.quote(discussion)

#de momento, el conteo de avisos no funciona para la wikipedia en español
configNotices = 0

pagesCommons = 1

galleryCommons = 1

wikisource = 1

wikiverse = 1

wikibooks = 1

window = 1
#window template
windowTemplate="{{artículo destacado"

quality = 1
#voice di quality template
vdqTemplate="{{artículo bueno"

sifter = 1

bibliography = 1

coordinate = 1


def get_avg_pageviews(voice, start, end):
  SUM = 0;

  try:

    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"+language+".wikipedia/all-access/user/"+voice+"/daily/"+start+"/"+end
   
    html = urlopen(url).read()



    html = str(html);

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
    res = str(int(round((SUM/days),0)))

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

  voice = voice.replace(" ","_")

  SUM = 0

  try:

    url ="https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"+language+".wikipedia/all-access/user/"+voice+"/daily/"+START_ALL_TIME +"/" + END_CURRENT_YEAR

    html = urlopen(url).read()

    etc = 0 # da cambiare

    if etc == 0:

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
  res3 = get_avg_pageviews(voice, START_PREV_YEAR, END_PREV_YEAR)

  #calculate res4, average pageviews from current year
  res4 = get_avg_pageviews(voice, START_CURRENT_YEAR, END_CURRENT_YEAR)

   
  return str(res1), str(res2), str(res3), str(res4)





def firstname2Q(item):

  return item.getID()





def note(text):

  return str(text.count('</ref>'))





def dimension(text):
  return str(len(text))





def images(text):

  t = text.lower()

  img = str(t.count('.jpg')+t.count('.svg')+t.count('.jpeg')+t.count('.png')+t.count('.tiff')+t.count('.gif')+t.count('.tif')+t.count('.xcf'))

  return img





def primoEdit(voice):

  try:

    url ="https://xtools.wmflabs.org/api/page/articleinfo/"+language+".wikipedia.org/"+voice.replace(" ","_")
    html = urlopen(url).read()

    html = str(html)

    html = html[html.find("created_at")+len("created_at")+3:]

    html = html[:10]

  except:

    html= "ERRORE"

  return html





def Notices(t):

   t_tmp =t

   t = t.replace("\n","")

   t = t.replace(" ","")

   t = t.lower()

    

   tmpcheck = t.count('{{c|') + t.count('{{c}}')

   tmpsynoptic = t.count('{{tmp|')  + t.count('{{tmp}}')

   tmphelp = t.count('{{a|')

   tmpcorrect = t.count('{{correct')

   tmpcuriosity = t.count('{{curiosit')

   tmpdivide = t.count('{{d|') + t.count('{{d}')

   tmpsources = t.count('{{f|')  + t.count('{{f}}')

   tmplocal = t.count('{{l|')  + t.count('{{l}}')

   tmpPOV = t.count('{{p|')  + t.count('{{p}}')

   tmpNN = t.count('{{nn|')  + t.count('{{nn}}')

   tmprecent = t.count('{{recent')

   tmpmanual = t.count('{{stilemanualistico')

   tmptranslation = t.count('{{t|')  + t.count('{{t}}')

   tmpwikify = t.count('{{w|')  + t.count('{{w}}')

   tmpstub = t.count('{{s|')  + t.count('{{s}}')

   tmpstubsection = t.count('{{stubsection')

   tmpcontrolcopi = t.count('{{controlcopy')



   SUMNotices = tmpcheck + tmpsynoptic + tmphelp + tmpcorrect + tmpcuriosity + tmpdivide + tmpsources + tmplocal + tmpPOV

   SUMNotices = SUMNotices + tmpNN + tmprecent + tmpmanual + tmptranslation + tmpwikify + tmpstub + tmpstubsection + tmpcontrolcopi



   tmpwithoutsources = t.count('{{withoutsource') + t.count('{{citazionenecessaria') + t.count('{{withoutsource}}') + t.count('{{citazionenecessaria}}')

   tmpclarify = t.count('{{clarify') + t.count('{{clarify}}')



   return str(SUMNotices), str(tmpwithoutsources), str(tmpclarify)





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





def lengthStart(text):

   start = text

   start = start[:start.find("\n==")]

   ntemplate  =start.count('{{')

   startclear = start

   fn = start.count("{{formatnum:")

   for i in range(fn):

      tmp = start[start.find("{{formatnum:"):]

      tmp = tmp[:tmp.find("}}")+2]

      tmp2 = tmp.replace("{{formatnum:","")

      tmp2 = tmp2.replace("}}","")

      start = start.replace(tmp, tmp2)



   ntemplate = start.count("{{")

   for i in range(ntemplate):

      text = start[start.find("{{"):]

      template = findtemplate(text)

      text = text.replace("{{"+template,"")

      start = start.replace("{{"+template,"")

   start = start.replace("</ref>","")

   n = start.count("<ref")

   for i in range(n):

      tmp = start[start.find("<ref"):]

      tmp = tmp[:tmp.find(">")+1]

      start = start.replace(tmp,"")

   start = start.replace("[[","")

   start = start.replace("]]","")

   start = start.replace("|","")

   lunstart = len(start)
   return str(lunstart)





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





    

def analyse():
   f = open('query.csv', "r")

   vox = f.readlines()   
    
   # eliminare il contenuto del file prima di iniziare
   results = open('results.txt',"w")
   results.truncate(0)
   results.close()

   for voice in vox:
      
      results = open('results.txt', 'a')  # aprire il file in modalità di aggiunta

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

        res = res + voice +"\t" +"voice inesistente"

       

      else:

        if primoEdit:

           res = res + primoEdit(voice2) + "\t"



        if dimension:

           res = res + dimension(wikitext) + "\t"



        if images:

           res = res + images(wikitext) + "\t"



        if note:

           res = res + note(wikitext) + "\t"

           

        if configNotices:

           for i in Notices(wikitext):
              print("some avisi")
              res = res + i + "\t"

               

        if dimensionDiscussion:

           res = res + dimension(wikitext_discussion) + "\t"



        if dimensionStart:

           res = res + lengthStart(wikitext) + "\t"

           

        if visits:

           for i in visits(voice2):

              res = res + i + "\t"



        if vdq:

           res = res + vdq(wikitext) + "\t"



        if window:

           res = res + window(wikitext) + "\t"



        if galleryCommons:

           try:

              res = res + wikidata["entities"][wikidataid]["claims"]["P373"][0]["mainsnak"]["datavalue"]["value"] + "\t"

           except:

              res = res + "" + "\t"



        if pagesCommons:

           try:

              res = res + wikidata["entities"][wikidataid]["claims"]["P935"][0]["mainsnak"]["datavalue"]["value"] + "\t"

           except:

              res = res + "" + "\t"

   

        if wikisource:

           try:

              res = res + wikidata["entities"][wikidataid]["sitelinks"]["wikisource"]["title"] + "\t"

           except:

              res = res + "\t"



        if coordinate:

           try:

              res = res + wikidata["entities"][wikidataid]["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]["latitude"] + "\t"

              res = res + wikidata["entities"][wikidataid]["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]["longitude"] + "\t"

           except:

              res = res + "\t" + "\t"

      results.write(res + "\n")  # aggiungere un salto di linea dopo ogni resultato
      results.close()  # chiudere il file
      print (res)

     

def main():

   analyse()



if __name__ == "__main__":

   main()
