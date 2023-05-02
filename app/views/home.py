from app import app
from flask import render_template

from app.services.fetcher.api_fetcher.fetcher_category_list import FetcherCategoryList

# Defines a route for the home page and renders a template with a list of categories fetched from a product crawler.
@app.route("/", methods=["GET", "POST"])
def index():
    try:
        fetcher_category_list = FetcherCategoryList()
        category_list = fetcher_category_list.fetch_category_list()
        return render_template("public/index.html", category_list=category_list)
    except Exception as e:
        return render_template("public/error.html", message=e)
