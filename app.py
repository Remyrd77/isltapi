import flask
from flask import request,render_template
import pandas as pd
from flask_cors import CORS, cross_origin
import os

csv_path = "./ISLT_data.csv" # file should be saved somewhere else, should not be a part of build folder
def readCSV():
    cols=["pg","word","definition","sentence","category","sample","synonyms"]
    data = pd.read_csv(csv_path, sep=',', usecols=cols,na_values = [''])
    return data
def retrieveData():
    data = readCSV()
    json_data = data.to_json(orient = "records")
    json_list = json_data.replace("\\","")
    print(json_list)
    return json_list


app = flask.Flask(__name__,template_folder='template')
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

print('***Backend Running***')

@app.route('/')
def home():
    return render_template('create.html')

@app.route('/getData',methods=['GET'])
def getData():
    return retrieveData()

@app.route('/sendData', methods=['GET','POST']) 
@cross_origin()
def sendData():
    if request.method == "POST":
        postData= pd.json_normalize(request.form)
        data = readCSV()
        newData = pd.concat([data,postData],ignore_index=True)
        # adding new data into csv
        os.remove(csv_path)
        newData.to_csv(csv_path,index=False)
        print(postData)
    return request.form