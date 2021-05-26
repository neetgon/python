import time, threading, os, math;
from flask import Flask, render_template, url_for, json, url_for, request, redirect;
from werkzeug.utils import secure_filename;

app = Flask(__name__);

files = [];
files_remove = []

def add_file():
    global files;
    files = [];

    path = "static/files";

    try:
        if(os.path.exists(path)):
            for f in os.listdir(path):
                type = "";

                for i in f[::-1]:
                    if(i) != ".":
                        type += i;
                    else:
                        break;

                type = type[::-1];
                type = type.upper()

                file_size = os.path.getsize("{}/{}".format(path, f))

                file_mega = file_size / (1024 * 1024);
                file_giga = file_size / (1024 * 1024 * 1024);

                size = None;
                size_type = None;

                if file_mega > 1:
                    size_type = "MB";
                    size = file_mega;
                else:
                    size_type = "KB";
                    size = file_size * 0.001;

                if file_mega > 1024:
                    size_type = "GB";
                    size = file_giga;

                size = round(size);

                name = f;
                name = name.replace("." + type.lower(), "");

                files.append({"name": name, "type": type, "size": size, "size_type": size_type});
    except:
        pass

def add_file_from_remove():
    global files_remove;
    files_remove = [];

    path = "static/remove";

    try:
        if(os.path.exists(path)):
            for f in os.listdir(path):
                type = "";

                for i in f[::-1]:
                    if(i) != ".":
                        type += i;
                    else:
                        break;

                type = type[::-1];

                file_size = os.path.getsize("{}/{}".format(path, f))

                file_mega = file_size / (1024 * 1024);
                file_giga = file_size / (1024 * 1024 * 1024);

                size = None;
                size_type = None;

                if file_mega > 1:
                    size_type = "MB";
                    size = file_mega;
                else:
                    size_type = "KB";
                    size = file_size * 0.001;

                if file_mega > 1024:
                    size_type = "GB";
                    size = file_giga;

                size = round(size);

                name = f;
                name = name.replace("." + type.lower(), "");

                files_remove.append({"name": name, "type": type, "size": size, "size_type": size_type});
    except:
        pass

def update_files(loop):
    if not loop:
        add_file();
        add_file_from_remove();
    else:
        while loop:
            try:
                add_file();
                add_file_from_remove();
            except:
                pass

            time.sleep(3);

@app.route('/delete/<file>', methods=['GET'])
def delete(file):
    try:
        path = "static/remove";
        os.remove("{}/{}".format(path, file));
        add_file();
        add_file_from_remove();
        return redirect("/");
    except:
        pass

    return render_template('upload/main.html', files=files, remove=files_remove);

@app.route('/remove/<file>', methods=['GET'])
def remove(file):
    path = "static/files";
    file_path = "{}/{}".format(path, file);
    destination = "{}/{}".format("static/remove", file);

    os.replace(file_path, destination);

    add_file();
    add_file_from_remove();
    return redirect("/");

    return render_template('upload/main.html', files=files, remove=files_remove);

@app.route('/recover/<file>', methods=['GET'])
def recover(file):
    path = "static/files";
    file_path = "{}/{}".format(path, file);
    destination = "{}/{}".format("static/remove", file);

    os.replace(destination, file_path);

    add_file();
    add_file_from_remove();

    return redirect("/");

    return render_template('upload/main.html', files=files, remove=files_remove);

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        for f in request.files.getlist('files'):
            savePath = "static/files/" + secure_filename(f.filename);
            f.save(savePath);

        update_files(False);

    return render_template('upload/main.html', files=files, remove=files_remove)

if __name__ == '__main__':
    threading.Thread(target=update_files, args=(True,)).start();
    app.run(host="0.0.0.0", port=2304, debug=True);
