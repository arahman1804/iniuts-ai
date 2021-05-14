from flask import Flask, render_template, request
import requests
from urllib.parse import urlparse
from textblob import TextBlob 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def awal():
    if request.method == 'POST': 

        link = request.form['link']
        ai = urlparse(link)
        ai.query
        pidio = ai.query[2:]

        URL = "https://www.googleapis.com/youtube/v3/commentThreads"
        API_KEY = "AIzaSyA9tS7UDYUU94jpLKW6b1jnjRfDZf5jmYE"
        VIDEO_ID = pidio

        response = requests.get(f"{URL}?key={API_KEY}&videoId={VIDEO_ID}&part=snippet")
        response_json = response.json()

        comments = []
        commentsnya = []
        penulis = []
        i = 0

        #pengulangan dari data json
        for item in response_json["items"]:
            if i <= 5:
                author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                content = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                published_at = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
               
                penulis.append(author)
                commentsnya.append(content)
                
                i += 1
            else :
                break
        
        kategori = []

        #cek sentimen 
        for i in commentsnya:
            sentimen = TextBlob(i).sentiment.polarity
            if sentimen < 0:
                kategori.append("Kommentar berbau negatif")
            elif sentimen == 0:
                kategori.append("Kommentar masih dalam keadaan normal")
            else :
                kategori.append("Komentar yang sangat positif")

        return render_template('index.html', link = link, kategori = kategori, penulis = penulis, commentsnya = commentsnya)
    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)
