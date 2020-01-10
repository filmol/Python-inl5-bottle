# coding: utf-8
# Author: Filip Moltzer
#TODO RESPONSIVE

from bottle import route, run, template, request, static_file, error
import os 
from os import path
wiki_dir = "/Users/filipmoltzer/Desktop/inl-5/wiki"

def get_articles(): 
    """ Fetches all the articles"""
    articles = []

    #Loops trough each file in wiki directory and appends the file name (-.txt) the articles list if it's a txt file.
    for f in os.listdir(wiki_dir):
        if f.endswith('.txt'):
            f = f.replace(".txt", "")
            articles.append(f)

    articles.pop(0) #Removes a unwanted empty list element.
    return articles

def get_file(pagename):

    my_file = open("wiki/"+pagename+".txt","r")    

    text = [] 
    for row in my_file.read().split("\n"): 
        text.append(row)
    return text

@route("/")
def index():
    """
    This is the home page, which shows a list of links to all articles
    in the wiki.
    """
    return template("index", articles = get_articles())


@error(404)
def error404(error):
    """
    Returns a good looking error template with options to go back to start or create a new article.  
    """
    return template("error")

@route('/wiki/<pagename>/')
def show_article(pagename):
    """Displays a single article (loaded from a text file)."""
    return template("article", file = get_file(pagename), pagename = pagename)
   
@route('/static/<filename>')
def static_files(filename):
    return static_file(filename, root="static")


@route('/edit/')
def edit_form():
    """
    Shows a form which allows the user to input a title and content
    for an article. This form should be sent via POST to /update/.
    """
    return template("edit") #TODO

@route('/remove/')
def remove_form():
    """
    Shows a form which allows the user to input a title to be deleted.
    This form should be sent via POST to /remove_update/.
    """
    return template("remove") #TODO

@route('/update/', method="POST")
def update_article():
    """
    Receives page title and contents from a form, and creates/updates a
    text file for that page.
    """
    subject = request.forms.get("Titel")
    content = request.forms.get("content")
    img = request.forms.get("Image:")

    
    #Öppna upp txt filen med namnet "subject" om den redan finns, annars skapa en ny.
    try: 
        my_file = open("wiki/"+subject+".txt","a")
        my_file.write("\n" + content)
        my_file.close()
    except:
        my_file = open("wiki/"+subject+".txt","w").close()
        my_file = open("wiki/"+subject+".txt","r")
        my_file.write(content)
        my_file.close()

    return template("article", file = get_file(subject), pagename = subject, img = img)

@route('/remove_update/', method="POST")
def remove_article():
    subject = (request.forms.get("Titel")+".txt")
    print(subject)
    
    try:
        for f in os.listdir(wiki_dir):
            if f == subject:
                os.remove("/Users/filipmoltzer/Desktop/inl-5/wiki/"+subject)
                return template("index", articles = get_articles())
        return false
    except:
        return template("error")
    
run(host='localhost', port=8080, debug=True, reloader=True)
