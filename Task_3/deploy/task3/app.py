import pandas as pd
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, send_file, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DOWNLOAD_FOLDER = 'downloads/'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


@app.route('/')
def index():
    return redirect('/uploadfile')


@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            df = pd.read_csv(UPLOAD_FOLDER + filename, sep=',')
            cols = ["order_purchase_year", "order_purchase_month", "order_purchase_day"]
            order_date = pd.to_datetime(df[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")) \
                         + df['order_purchase_hour'].apply(pd.offsets.Hour)
            predictions_hours = model.predict(df).astype(int)
            predicted_delivery_date = order_date + pd.Series(predictions_hours).apply(pd.offsets.Hour)
            res = pd.DataFrame(predicted_delivery_date, columns=["predicted_delivery_date"])
            res.to_csv(DOWNLOAD_FOLDER + 'result.csv', index=False)
            return redirect('/downloadfile/'+ 'result.csv')
    return render_template('upload_file.html')


@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    return render_template('download.html', value=filename)


@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = DOWNLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True)


if __name__=="__main__":
    app.run(debug=True)