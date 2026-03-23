from flask import Flask, render_template, request
from search import searchEngine  # put your class in search_engine.py

app = Flask(__name__)

searcher = searchEngine("movies copy.csv")
searcher.readDatabase()
searcher.createInvertedIndex()
searcher.createTree()

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""

    if request.method == "POST":
        query = request.form["query"]
        results = searcher.search(query)

    return render_template("index.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)
    print("Server is running on http://localhost:5000")