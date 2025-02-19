import flask
import os

###############################################################################

# Initialize Flask.
app = flask.Flask(__name__)
# The secret key is used to encrypt the cookie, it's needed to make sessions work.
# For this application it doesn't need to be super secure. For better security use 
# the secrets module and secrets.token_hex()
app.secret_key = "12345"

MEDIA_PATH = "/media/" + os.getlogin() + "/"

###############################################################################

def getSongList(genre):
    genresFolder = getGenresFolder()
    if (len(genresFolder) == 0):
        return []
    
    songlist = os.listdir(os.path.join(genresFolder, genre))
    songlist.sort()
    return songlist

###############################################################################

def getCurrentSongName(songlist, index):
    if (index < 0) or (index >= len(songlist)):
        return ""
        
    return songlist[index]

###############################################################################

def moveToNewSong(genre, currentIndex, increment=1):
    songlist = getSongList(genre)
    if (len(songlist) == 0):
        return 0
    
    newIndex = currentIndex + increment
    
    if (newIndex >= len(songlist)):
        newIndex = 0
    if (newIndex < 0):
        newIndex = len(songlist) - 1
    return newIndex

###############################################################################

def getGenresFolder():
    # drive should have folder named "genres", use the first drive with that folder
    drives = os.listdir(MEDIA_PATH)
    for drive in drives:
        drivePath = os.path.join(MEDIA_PATH, drive)
        if ("genres" in os.listdir(drivePath)):
            genresFolder = os.path.join(drivePath, "genres")
            return genresFolder
    
    return ""

###############################################################################

def getGenres():
    genresFolder = getGenresFolder()
    if (len(genresFolder) == 0):
        return []
        
    genres = os.listdir(genresFolder)
    genres.sort()
    return genres

###############################################################################

@app.route("/")
def mainPage():
    genres = getGenres()
    return flask.render_template('index.html', genres=genres)

###############################################################################

@app.route("/player")
def genrePlayer():
    genre = flask.request.args.get("genre")
    currentIndex = flask.session.get(genre, 0)
    songlist = getSongList(genre)
    songname = getCurrentSongName(songlist, currentIndex)
    return flask.render_template("player.html", songname=songname, genre=genre, songlist=songlist)

###############################################################################

@app.route("/song")
def sendFile():
    filename = flask.request.args.get("filename")
    filename = filename.replace("&amp;", "&") # rendering the template will change & to &amp; so change it back
    genresFolder = getGenresFolder()
    genre = flask.request.args.get("genre")
    return flask.send_from_directory(os.path.join(genresFolder, genre), filename)

###############################################################################

@app.route("/next")
def nextSong():
    genre = flask.request.args.get("genre")
    currentIndex = flask.session.get(genre, 0)
    newIndex = moveToNewSong(genre, currentIndex, 1)
    flask.session[genre] = newIndex
    flask.session.permanent = True # make sure the cookie persists even after browser is closed
    return flask.redirect(f"/player?genre={genre}")

###############################################################################

@app.route("/prev")
def prevSong():
    genre = flask.request.args.get("genre")
    currentIndex = flask.session.get(genre, 0)
    newIndex = moveToNewSong(genre, currentIndex, -1)
    flask.session[genre] = newIndex
    flask.session.permanent = True # make sure the cookie persists even after browser is closed
    return flask.redirect(f"/player?genre={genre}")
    
###############################################################################

@app.route("/seek")
def seekSong():
    genre = flask.request.args.get("genre")
    seekIndex = flask.request.args.get("seekIndex")
    try:
        flask.session[genre] = int(seekIndex)
    except:
        flask.session[genre] = 0
    flask.session.permanent = True # make sure the cookie persists even after browser is closed
    return flask.redirect(f"/player?genre={genre}")

###############################################################################

if __name__ == "__main__":
    app.run("0.0.0.0", 6513)
