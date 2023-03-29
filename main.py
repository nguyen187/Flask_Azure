from flask import *

import pandas as pd
import os
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient

storage_account_key = "5dLVgbOA1ADjScKtKuJXNZUohV3ml7HS0XezwIjgkPhYi+VArRO4KGvL3fP3R3RQSWDlHxMYrKXx+ASt1FpTqQ=="
storage_account_name = "demov1"
connection_string = "DefaultEndpointsProtocol=https;AccountName=demov1;AccountKey=5dLVgbOA1ADjScKtKuJXNZUohV3ml7HS0XezwIjgkPhYi+VArRO4KGvL3fP3R3RQSWDlHxMYrKXx+ASt1FpTqQ==;EndpointSuffix=core.windows.net"
container_name = "containerdemov1"

def upload_To_BlobStorage(file_path,file_name):
    try:
        blob_service = BlobServiceClient.from_connection_string(connection_string)
        print(file_name)
        blob_client = blob_service.get_blob_client(container = container_name,blob = file_name)
        with open(file_path,"rb") as data:
            blob_client.upload_blob(data)
        print('uploaded'+file_name+"file")
        alert = '<div style="color: green;">File uploaded successfully</div>'
        return alert
    except:
        alert = '<div style="color: red;">File upload Existed</div>'
        return alert
#*** Flask configuration
 

app = Flask(__name__)
 
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.getcwd() + '/static/upload'
# RESULT_FOLDER = os.getcwd() + '/static/img_result/'
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/',  methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
       # session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)
        uploaded_file = request.files['uploaded-file']
        filename = secure_filename(uploaded_file.filename)

        # Lưu nội dung file upload vào file tạm
        uploaded_file.save(os.path.join(UPLOAD_FOLDER, filename))
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        # Gọi hàm upload file tới Blob Storage
        
        alert = upload_To_BlobStorage(file_path, filename)

        # Xóa file tạm
        os.remove(file_path)

        # Render template with active link
        
        return render_template('index.html', active_link=Markup('home'), alert=Markup(alert))
    return render_template('index.html', active_link='home')
if __name__=='__main__':
    app.run(host="0.0.0.0",port = 80)
