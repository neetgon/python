import time, threading, os
from flask import Flask, render_template, url_for, json, url_for, request
app = Flask(__name__)

catalog = {}

def catalog_update():
    global catalog
    
    try:
        while True:
            local_catalog = {};
            
            for title in os.listdir("catalog"):
                    with open('catalog/{}'.format(title), 'r') as fp:
                        c = json.load(fp);
                        local_catalog.update(c);
            
            catalog = local_catalog;
            time.sleep(5);
    except:
        print("Caralho deu erro de novo nessa porra");

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template("catalog/main.html", catalog=catalog, id = "attack-on-titan")

@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    if path in catalog:
        return render_template('catalog/main.html', catalog = catalog, id=path)
    else:
        return render_template('main/main.html')

if __name__ == '__main__':
    threading.Thread(target=catalog_update, args=()).start()
    app.run(host="0.0.0.0", port=5000, debug=True)
