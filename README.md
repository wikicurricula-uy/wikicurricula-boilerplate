# A Step-By-Step Guide on How To Locally Install the Wikicurricula Boilerplate on Your Computer.

This is a giude on how to install the Wikicurricula boilerplate on your local machine as a beginner.


## Introduction
Wikicurricula is an Interactive tool that helps visualize national curriculum data stored in Wikidata. It also shows metrics about Wikipedia articles that are relevant to the curriculum.
This is a boilerplate that will support the implementations in several countries and languages.


Credits to Wikipedia e Scuola Italiana for the original implementation.
Idea and leadership: Iolanda pensa
Web design and visualisation by Giovani Profeta - [repo](https://github.com/giovannipro/giovannipro.github.io/tree/master/wikipedia-scuola-italiana)
Work group: Federico Benvenuti, Valerio Iannucci, Luca Martinelli, Paolo Fichera
Support and collaboration: [Wikimedia Italia](https://www.wikimedia.it/)


## Setting up your Environment

Before being able to install and start the folder, you must have the necessary development environments.

  - A github account
   -If you don't already have one, you can do so here [Github.com](github.com)
   
  - A code editor
   - To enable you open and view the content of the folder, you need a code editor. Visual Studio code is one of the 
     most popular code editors around. You can install one here [VSCode.com](https://code.visualstudio.com/download)
  
  - A strong internet connection
    - This is to make sure you don't have a break in connection throught out the process.



## Installing the Boilerplate

1. First you have to go to the Wikicurricula [github repository](https://github.com/wikicurricula-uy/wikicurricula-boilerplate).

2. Fork the repository into your github.

3. Clone your fork of the repository into your local machine.
  NB: Make sure not to clone the direct repository from wikicurricula as this would throw up errors in the future. The URL for cloning
  should include your username e.g `https://github.com/yourUSERNAME/wikicurricula-boilerplate`

4. To clone the repo to your local machine:
   - open the command line interface of your computer(e.g powershell or CMD for windows).
   - Run "git clone github repo URL" e.g `git clone https://github.com/yourUSERNAME/wikicurricula-boilerplate`
   - Change directory into the just cloned folder by running `cd wikicurricula-boilerplate`
   - If you have VSCode installed, run `code .`, this will automatically open the folder and now you can view the files inside.

 ## Running files

 Both the `autori` and the `visulization` folders contain HTML files that can be run on your browser.
 The convention is to find the files through your computer's file explorer and double click to open.
 A much easier and time saving way is to use the VSCode Liver server extension. To do this:
   - Install the `Live Server` in the extesnions marketplace.
   - Open the HTML file
   - Right click on the file.
   - Among the options click on `Open with Live Server`.
    This will automatically run the file on your browser using a default local host port. Now you can view the UI of Wikicurricula's boilerplate!

# Credits
Credits to Wikipedia e Scuola Italiana for the original implementation.
Idea and leadership: Iolanda pensa
Web design and visualisation by Giovani Profeta - [repo](https://github.com/giovannipro/giovannipro.github.io/tree/master/wikipedia-scuola-italiana)
Work group: Federico Benvenuti, Valerio Iannucci, Luca Martinelli, Paolo Fichera
Support and collaboration: [Wikimedia Italia](https://www.wikimedia.it/).