import flask
import re
import requests
from headers import headers
a = flask.Flask(__name__)
@a.route('/')
def home():
    return flask.render_template("c/home.html")    
@a.route("/", methods=["GET", "POST"])
def post():
    l = flask.request.form["q"]
    if flask.request.method == "POST":
        with open("_", "wb") as a1:
            a1.write(bytes(l.encode()))
    return flask.render_template("c/home.html") and flask.redirect("/content/play")
@a.route('/about')
def about():
    return flask.render_template("x/about.html")
@a.route("/contact")
def contact():
    return flask.render_template("z/contact.html")
@a.route("/favicon.ico")
def con():
    return flask.render_template("v/ico.html")
@a.route("/content/play")
def api():   
    with open("_", 'r') as q1:
        try:
            w = q1.read()
            req1 = requests.get("https://useraction.zee5.com/tokennd").json()
            rgx = re.findall("([0-9]?\w+)", w)[-3:]
            li = { "url":"zee5vodnd.akamaized.net", "token":"https://gwapi.zee5.com/content/details/" }
            req2 = requests.get("https://useraction.zee5.com/token/platform_tokens.php?platform_name=web_app").json()["token"]
            headers["X-Access-Token"] = req2
            req3 = requests.get("https://useraction.zee5.com/token").json()
            htm = """
                <!DOCTYPE html>
                <html>
                    <meta name="viewport" content="width=device-width, initial-scale=1" />
                    <title> {} </title>
                    <body>
                        <div align = "center">
                           <body style="background-color:black;">
                            <div id = "img" align = "center">
                                <img src = '{}'/>
                            </div>
                            <div id = "text" style = "color:grey">
                                {}  ¤ {}
                                <p <b> Rating : {} | Duration : {} secs</b></br></br>
                                 {} </b></p></br>
                            </div>
                            <button onclick="document.location='{}'">play</button>
                        </div>
                    </body>
                </html>
                """                               
            if "movies" in w:
                r1 = requests.get(li["token"] + "-".join(rgx),
                                            headers=headers, 
                                            params={"translation":"en", "country":"IN"}).json()
                g1 = (r1["hls"][0].replace("drm", "hls") + req1["video_token"])
                return htm.format(r1["title"], r1["image_url"], r1["title"], 
                                    r1["age_rating"], r1["rating"], r1["duration"], 
                                    r1["description"], "https://" + li["url"] + g1)
            elif "tvshows" or "originals" in w:
                r2 = requests.get(li["token"] + "-".join(rgx), 
                                            headers=headers, 
                                            params={"translation":"en", "country":"IN"}).json()
                g2 = (r2["hls"][0].replace("drm", "hls"))
                if "netst" in g2:
                    return htm.format(r2["title"], r2["image_url"], r2["title"], r2["age_rating"],
                                      r2["rating"], r2["duration"], r2["description"], 
                                      g2 + req3["video_token"])
                else:
                    return htm.format(r2["title"], r2["image_url"], r2["title"], r2["age_rating"], 
                                            r2["rating"], r2["duration"], r2["description"], 
                                            "https://" + li["url"] + g2 + req1["video_token"])
            else:
                pass
        except IndexError:
            return flask.jsonify({ "message" : "No url specified" }), 200
        except requests.exceptions.ConnectionError:
            return flask.jsonify({ "message" : "No connection" })
        except KeyError:
            return { "message" : "Try Again" }, 200
if __name__ == "__main__":
    a.run("127.0.0.1", 8080, debug=True)