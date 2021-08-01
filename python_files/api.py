import flask
from flask import Flask, request, url_for, Response, jsonify
import pymongo
import json
import requests
import re
import numpy as np
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO
from base64 import b64encode

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def black_color_func(word, font_size, position, orientation, random_state = None, **kwargs):
    return("hsl(0,100%, 1%)")

ceo = [re.compile(r'.*Chief Executive Officer'), re.compile(r'.*CEO$')]
cfo = [re.compile(r'.*Chief Financial Officer'), re.compile(r'.*CFO$')]
coo = [re.compile(r'.*Chief Operating Officer'), re.compile(r'.*COO$')]
cao = [re.compile(r'.*Chief Accounting Officer'), re.compile(r'.*CAO$')]
cto = [re.compile(r'.*Chief Technical Officer'), re.compile(r'.*CTO$')]
cmo = [re.compile(r'.*Chief Managing Officer'), re.compile(r'.*CMO$')]

clo = [re.compile(r'.*Chief Legal Officer'), re.compile(r'.*CLO$')]
cio = [re.compile(r'.*Chief Information Officer'), re.compile(r'.*CIO$')]
cco = [re.compile(r'.*Chief Communications Officer'), re.compile(r'.*CCO$')]
cdo = [re.compile(r'.*Chief Development Officer'), re.compile(r'.*CDO$')]
ctecho = [re.compile(r'.*Chief Technology Officer')]
cmarko = [re.compile(r'.*Chief Marketing Officer')]
cso = [re.compile(r'.*Chief Sales Officer')]

ciso = [re.compile(r'.*Chief Information Security Officer'), re.compile(r'.*CISO$')]
chro = [re.compile(r'.*Chief Human Resource Officer'), re.compile(r'.*Chief Human Resources Officer'), re.compile(r'.*CHRO$')]
ccompo = [re.compile(r'.*Chief Compliance Officer')]

cSuite_titles = {'ceo':ceo, 'cfo':cfo, 'coo':coo, 'cao':cao, 'cto':cto, 'cmo':cmo, 'clo':clo, 'cio':cio, 'cco':cco, 'cdo':cdo, 'ctecho':ctecho, 'cmarko':cmarko, 'cso':cso, 'ciso':ciso, 'chro':chro, 'ccompo':ccompo}

cluster_uri = 'mongodb+srv://Balasankar:balasankar01@cluster0.k4d0t.mongodb.net/Fortune1000?retryWrites=true&w=majority'
comp_client = pymongo.MongoClient(cluster_uri)

comps = comp_client['Fortune1000']['basicDetails']
comps_newsArticles = comp_client['Fortune1000']['NewsArticles']
comps_key = comp_client['Fortune1000']['TopKeywordsAndWeights']
comps_cSuite = comp_client['Fortune1000']['CSuite_Neat']

companies = []
for x in comps.find():
    del x['_id']
    companies.append(x)

companies_newsArticles = []
for x in comps_newsArticles.find():
    del x['_id']
    companies_newsArticles.append(x)

companies_key = []
for x in comps_key.find():
    del x['_id']
    companies_key.append(x)

companies_cSuite = []
for x in comps_cSuite.find():
    del x['_id']
    companies_cSuite.append(x)


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Companies Info</h1>
<p>A prototype API for obtaining the details of the companies.</p>
<p>Use 
<a href="http://127.0.0.1:5000/api/v1/resources/companies/all">1</a> to get the details of all the companies.</p>
<p>Use <a href="http://127.0.0.1:5000/api/v1/resources/companies/id?name={}&ind={}">2</a> to get the ID of the companies satisfying the criteria.</p>
<p>Use <a href="http://127.0.0.1:5000/api/v1/resources/companies?id={}">3</a> to get the details of the specific company.</p>
<p>Use <a href="http://127.0.0.1:5000/api/v1/resources/companies/csuite?id={}&title={}">4</a> to get the Employee details for the specific company and Position/Title.</p>
<p>Use <a href="http://127.0.0.1:5000/api/v1/resources/companies/filter?ind={}&revAbove={}&revBelow={}">5</a> to get the details of the companies satisfying the criteria.</p>
<p>Use <a href="http://127.0.0.1:5000/api/v1/resources/companies/news?id={}">6</a> to get the news articles details of the specific company.</p>
<p>Use <a href="http://127.0.0.1:5000/api/v1/resources/companies/themes?id={}&count={}">7</a> to get the Top count number of themes for the specific company.</p>
'''


# API to get the Basic Details of all the companies.
@app.route('/api/v1/resources/companies/all', methods=['GET'])
def api_all():
    return jsonify(companies)


# API to get the ID of the company.
@app.route('/api/v1/resources/companies/id', methods=['GET'])
def api_getid():
    if 'name' in request.args:
        name = request.args['name'].lower()
    else:
        return "Error: No name field provided. Please provide the name of the company."

    ind_flag = 0
    if 'ind' in request.args:
        ind = request.args['ind'].lower()
        ind_flag = 1

    results = []

    for comp in companies:
        n = comp['Company'].lower()
        if(n.find(name) != -1 or name.find(n) != -1):
            if(ind_flag == 1):
                if(comp['Industry'].lower() == ind):
                    d = {}
                    d['ID'] = comp['Fortune1000_Rank']
                    d['Company'] = comp['Company']
                    d['Industry'] = comp['Industry']
                    results.append(d)
            else:
                d = {}
                d['ID'] = comp['Fortune1000_Rank']
                d['Company'] = comp['Company']
                d['Industry'] = comp['Industry']
                results.append(d)

    return jsonify(results)


# API to get the details of the company whose id is given as the input parameter.
@app.route('/api/v1/resources/companies', methods=['GET'])
def api_id():
    if 'id' in request.args:
        if(request.args['id'] == '{}'):
        	idx = 0
        else:
        	idx = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    results = []

    for comp in companies:
        comp_id = int(comp['Fortune1000_Rank'])
        if (comp_id == idx):
            results.append(comp)

    return jsonify(results)


# API to output the Company Employee details (the parameters are the company id and the title of the employee).
@app.route('/api/v1/resources/companies/csuite', methods=['GET'])
def api_csuite():
    if 'id' in request.args:
        if(request.args['id'] == '{}'):
        	idx = 0
        else:
        	idx = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    title_flag = 0
    if 'title' in request.args:
        title = request.args['title']
        title_flag = 1

    results = []

    for comp in companies_cSuite:
        comp_id = int(comp['Rank'])
        if (comp_id == idx):
            if(title_flag == 0):
                results.append(comp)
            else:
                comp_titles = list(comp.keys())
                d = {}
                for i in range(len(comp_titles)):
                    t = cSuite_titles[title]
                    for j in t:
                        if(j.match(comp_titles[i])):
                            d[comp_titles[i]] = comp[comp_titles[i]]

                results.append(d)

    return jsonify(results)


# API to filter the companies on the basis of industry and revenue.
@app.route('/api/v1/resources/companies/filter', methods=['GET'])
def api_filter():
    ind_flag = 0
    rA_flag = 0
    rB_flag = 0

    if 'ind' in request.args:
        ind = request.args['ind'].lower()
        ind_flag = 1
    if 'revAbove' in request.args:
        if(request.args['revAbove'] == "{}"):
        	rA = 0
        else:
        	rA = float(request.args['revAbove'])
        rA_flag = 1
    if 'revBelow' in request.args:
        if(request.args['revBelow'] == "{}"):
        	rB = 0
        else:
        	rB = float(request.args['revBelow'])
        rB_flag = 1

    results = []

    for comp in companies:
        comp_ind = comp['Industry']
        comp_rev = float(comp['Revenue (in Millions)'].replace('$','').replace(',',''))

        if(ind_flag == 1 and comp_ind.lower() == ind):
            if(rA_flag == 1 and comp_rev >= rA):
                if(rB_flag == 1 and comp_rev <= rB):
                    results.append(comp)
                elif(rB_flag == 0):
                    results.append(comp)
            elif(rA_flag == 0):
                if(rB_flag == 1 and comp_rev <= rB):
                    results.append(comp)
                elif(rB_flag == 0):
                    results.append(comp)
        elif(ind_flag == 0):
            if(rA_flag == 1 and comp_rev >= rA):
                if(rB_flag == 1 and comp_rev <= rB):
                    results.append(comp)
                elif(rB_flag == 0):
                    results.append(comp)
            elif(rA_flag == 0):
                if(rB_flag == 1 and comp_rev <= rB):
                    results.append(comp)
                elif(rB_flag == 0):
                    results.append(comp)

    return jsonify(results)


# API to get the Titles of the latest 100 News Articles of a company.
@app.route('/api/v1/resources/companies/news', methods=['GET'])
def api_news_id():
    if 'id' in request.args:
        if(request.args['id'] == '{}'):
        	idx = 0
        else:
        	idx = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    results = []

    for comp in companies_newsArticles:
        comp_id = int(comp['Rank'])
        if comp_id == idx:
            d = {}
            i = 0
            while(i < 100 and comp[str(i)] != None):
                d[str(i)] = comp[str(i)]
                i += 1
            d['Company'] = comp['Name']
            results.append(d)

    return jsonify(results)


# API to output the Top Themes/Keywords of a company 
# (parameters are the company id and count : No. of words to output, deafult is 10 and max is 100).
@app.route('/api/v1/resources/companies/themes', methods=['GET'])
def api_themes_id():
    if 'id' in request.args:
        if(request.args['id'] == '{}'):
        	idx = 0
        else:
        	idx = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    n_themes = 10

    if 'count' in request.args:
        if(request.args['count'] == '{}'):
        	n_themes = 0
        else:
        	n_themes = int(request.args['count'])

    results = []

    for comp in companies_key:
        comp_id = int(comp['Rank'])
        if comp_id == idx:
            d = {}
            i = 0
            i_max = min(len(list(comp.keys())) - 2, n_themes)

            while(i < i_max):
                d[str(i)] = comp[str(i)][0]
                i += 1
            d['Company'] = comp['Company']
            results.append(d)

    return jsonify(results)


@app.route("/api/v1/resources/companies/wordcloud", methods=['GET'])
def show_html():
    if 'id' in request.args:
        if(request.args['id'] == '{}'):
        	idx = 0
        else:
        	idx = int(request.args['id'])

    data = np.random.rand(80).reshape((2, 40))
    img = requests.post(
        request.scheme + "://" + request.host + url_for("img_gen"),
        json=json.dumps(data.astype(float).tolist()), data = {'id' : idx}
    ).content
    return b'<img src="data:image/png;base64,%b" />' %b64encode(img)


@app.route("/img/gen", methods=["POST"])
def img_gen():
    if 'id' in request.args:
        idx = int(request.args['id'])

    d = {}
    d_1 = companies_key[idx]
    length = len(list(d_1.keys())) - 2
    for i in range(length):
        a = d_1[str(i)]
        d[a[0]] = a[1]
    
    wordcloud = WordCloud(background_color = "white", width = 3000, height = 2000).generate_from_frequencies(d)
    wordcloud.recolor(color_func = black_color_func)
    fig = plt.figure(figsize = [10,10])
    plt.imshow(wordcloud, interpolation = "bilinear")
    plt.axis("off")
    
    png = BytesIO()
    FigureCanvasAgg(fig).print_png(png)
    plt.close(fig)
    return Response(png.getvalue(), mimetype="image/png")


app.run()