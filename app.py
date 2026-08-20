from flask import Flask, render_template, request, send_file

from search import search
from api import get_edition
from downloader import download_file


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search_books():

    query = request.args.get("q", "").strip()

    if not query:
        return render_template("index.html")

    results = search(query)

    return render_template(
        "results.html",
        query=query,
        results=results
    )


@app.route("/edition/<edition_id>")
def edition(edition_id):

    result = get_edition(edition_id)

    if result is None:
        return "Edition not found", 404

    return render_template(
        "edition.html",
        edition=result
    )

@app.route("/download/<file_id>")
def download(file_id):

    filename = download_file(file_id)

    return send_file(
        filename,
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)