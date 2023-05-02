import math, time, datetime

from app import app
from flask import redirect, render_template, request, session

from app.const.CONST import FETCH_TIKI_API_LIMIT
from app.services.fetcher.api_fetcher.fetcher_by_category import FetcherByCategory
from app.services.fetcher.api_fetcher.fetcher_by_keyword import FetcherByKeyword

from flask import render_template, session

# Previews a list of products based on the selected category or keyword inputted by the user.
@app.route("/preview", methods=["GET", "POST"])
def preview():
    # Store user_id and last_active in the session
    session['user_id'] = f'user-{time.strftime("%Y%m%d-%H%M%S")}'
    session['last_active'] = datetime.datetime.now()

    try:
        if request.method == "POST":
            req = request.form

            # Get category selected id, keyword and data size inputted by the user
            category_selected_id = req.get("category-id")
            keyword_inputted = req.get("keyword")
            data_size = int(req.get("data-size"))

            # `last_page`: the number of pages to fetch
            # `last_page_limit`: the limit of products to fetch on the last page
            last_page = math.ceil(data_size / FETCH_TIKI_API_LIMIT)
            last_page_limit = data_size - (last_page - 1) * FETCH_TIKI_API_LIMIT  

            # User did not select a category and enter a keyword
            if not category_selected_id and not keyword_inputted:
                return redirect("/")
            
            # User selected a category
            if category_selected_id:
                # User entered a keyword
                if keyword_inputted:
                    params = {
                        'page': last_page, 
                        'category': category_selected_id, 
                        'q': keyword_inputted, 
                        'limit': last_page_limit
                    }
                # User did not enter a keyword
                else:
                    params = {
                        'page': last_page, 
                        'category': category_selected_id, 
                        'limit': last_page_limit
                    }
                fetcher_by_category = FetcherByCategory(params)
                product_list = fetcher_by_category.fetch_by_category()
            # User did not select a category but entered a keyword
            elif keyword_inputted:
                params = {
                    'page': last_page, 
                    'q': keyword_inputted, 
                    'limit': last_page_limit
                } 
                fetcher_by_keyword = FetcherByKeyword(params)
                product_list = fetcher_by_keyword.fetch_by_keyword()
            else:
                return redirect("/")
            
            session['product_list'] = product_list
        else:
            return redirect("/")

        return render_template("public/preview.html", product_list=product_list)
    except Exception as e:
        return render_template("public/error.html", message=e)