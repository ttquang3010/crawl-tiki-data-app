from app import app
from flask import render_template, request, session, redirect

from app.services.saver.saver_as_csv import SaverAsCSV
from app.services.saver.saver_as_json import SaverAsJSON

# Saves product data in either CSV or JSON format based on user's choice.
@app.route("/save-data", methods=["GET", "POST"])
def save_data():
    
    req = request.form

    # Get path to save and file format by the user
    save_path = req.get("save-path")
    save_format = req.get("save-format")

    # Get product list to save to file
    data = session.get('product_list', [])

    saver_as_csv = SaverAsCSV(data, save_path)
    saver_as_json = SaverAsJSON(data, save_path)

    try:
        if request.method == "POST":
            if save_format == "csv":
                saver_as_csv.save()
            elif save_format == "json":
                saver_as_json.save()
            else:
                saver_as_csv.save()
        else:
            return redirect("/")

        return render_template("public/save_data.html")
    except Exception as e:
        return render_template("public/error.html", message=e)
    