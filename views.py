from flask import render_template, request
from app import app
from form import UrlForm
from anti_sensor import traffic, localization

@app.route("/model")
@app.route('/')
def homepage():
    print('routed correctly')
    form = UrlForm()
    return render_template('home.html',
                           title="Hamburglar!",
                           form=form)

@app.route("/results.html", methods=["post"])
def results():
    try:
        side1 = get_packets('side1')
        side2 = get_packets('side2')
        side2['Time'] = side2['Time'] + 10
        side3 = get_packets('side3')
        side3['Time'] = side3['Time'] + 20
        side4 = get_packets('side4')
        side4['Time'] = side4['Time'] + 30

        for i in [side1, side2, side3, side4]:
            preprocess(i)

        df = pd.concat([side1, side2, side3, side4])
        devices = all_device_stats(df)

        results = []
        for d in devices:
            results += (d, fit(d, int(request.form['Length']), int(request.form['Width'])))

        results = pd.DataFrame(dic(results)).to_html()

    except AssertionError:
        results = {'none': ['']}

    return render_template("results.html", data=results)
