# coding: utf-8
# Author: Filip Moltzer
from bottle import route, run, template, request, static_file, error
import os 
from os import path
wiki_dir = "wiki"

def get_articles(): 
    """ 
    Fetches and then returns all the articles in form of a list
    """
    articles = []
 
    # Loops trough each file in wiki directory, if it's a txt file: 1.Removes ".txt" 2.Appends the file to the articles list. 
    for f in os.listdir(wiki_dir):
        # BUG FIXED: Checks if the current file is a txt file before append to list 
        # Can't append ".DS_Store" file to the list that way.
        if f.endswith('.txt'):
            f = f.replace(".txt", "")
            articles.append(f)
    return articles

def get_file(pagename):
    """
    Fetches and returns the content of the the submitted txt file (pagename)
    """
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
    Returns a good looking error template with options to go back or create a new article.  
    """
    return template("error")

@route('/wiki/<pagename>/')
def show_article(pagename):
    """ 
    Displays a single article (loaded from a text file) 
    """
    return template("article", file = get_file(pagename), pagename = pagename)
   
@route('/static/<filename>')
def static_files(filename):
    return static_file(filename, root="static")


@route('/edit/<pagename>/')
def add_form(pagename):
    """
    Shows a form which allows the user to input a title and content
    for an article. This form should be sent via POST to /update/.
    """
    return template("edit", file = get_file(pagename), pagename = pagename)
    
@route('/add/')
def edit_form():
    """
    Shows a form which allows the user to input a title and content
    for an article. This form should be sent via POST to /update/.
    """
    return template("add")

@route('/remove/')
def remove_form():
    """
    Shows a form which allows the user to input a title to be deleted.
    This form should be sent via POST to /remove_update/.
    """
    return template("remove")

@route('/remove_this/<pagename>/')
def remove(pagename):
    """
    Recieves the subject information from current article.
    Then deletes the txt file from wiki folder if it does exist in there. (It should).
    """
    subject = (pagename+".txt")
    try:
        for f in os.listdir(wiki_dir):
            if f == subject:
                os.remove("wiki/"+subject)
                return template("index", articles = get_articles())
        return false
    except:
        return template("error")

@route('/update/', method="POST")
def update_article():
    """
    Receives page title and contents from a form, and creates/updates a
    text file for that page.
    """
    subject = request.forms.get("Titel")
    content = request.forms.get("content")
    
    #Öppna upp txt filen med namnet "subject" om den redan finns, annars skapa en ny.
    try: 
        my_file = open("wiki/"+subject+".txt","w")
        my_file.write("\n" + content)
        my_file.close()
    except:
        my_file = open("wiki/"+subject+".txt","w").close()
        my_file = open("wiki/"+subject+".txt","r")
        my_file.write(content)
        my_file.close()

    return template("article", file = get_file(subject), pagename = subject)

@route('/remove_update/', method="POST")
def remove_article():
    """
    Recieves the Titel information from the form.
    Then deletes the txt file from wiki folder if it does exist in there.
    """
    subject = (request.forms.get("Titel")+".txt")
    
    try:
        for f in os.listdir(wiki_dir):
            if f == subject:
                os.remove("wiki/"+subject)
                return template("index", articles = get_articles())
        return false
    except:
        return template("error")
    
run(host='localhost', port=8080, debug=True, reloader=True)
