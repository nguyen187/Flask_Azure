from flask import *

import pandas as pd
import os
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient

storage_account_key = "fI1afDCWKRqTzy2EWBFtN9XIexcKlLXP/RjTr5tFTdSSo4J8y5GJ+xzlYQmvin2eP626y8NRJQWo+AStvZ0Jww=="
storage_account_name = "flasktoblob"
connection_string = "DefaultEndpointsProtocol=https;AccountName=flasktoblob;AccountKey=fI1afDCWKRqTzy2EWBFtN9XIexcKlLXP/RjTr5tFTdSSo4J8y5GJ+xzlYQmvin2eP626y8NRJQWo+AStvZ0Jww==;EndpointSuffix=core.windows.net"

def load_photo():
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=connection_string)
    try:
        container_name = 'photos'
        container_client = blob_service_client.get_container_client(container=container_name)
        container_client.get_container_properties() # get properties of the container to force exception to be thrown if container does not exist
    except Exception as e:
        print(e)
        print("Creating container...")
        container_client = blob_service_client.create_container(container_name) # create a container in the storage account if it does not exist
        
    blob_items = container_client.list_blobs() # list all the blobs in the container

    img_html = "<div style='display: flex; justify-content: space-between; flex-wrap: wrap;'>"

    for blob in blob_items:
        blob_client = container_client.get_blob_client(blob=blob.name) # get blob client to interact with the blob and get blob url
        img_html += "<img src='{}' width='auto' height='200' style='margin: 0.5em 0;'/> ".format(blob_client.url) # get the blob url and append it to the html

    img_html += "</div>"
    return img_html

def load_file():
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=connection_string)
    try:
        container_name = 'test1'
        container_client = blob_service_client.get_container_client(container=container_name)
        container_client.get_container_properties() # get properties of the container to force exception to be thrown if container does not exist
    except Exception as e:
        print(e)
        print("Creating container...")
        container_client = blob_service_client.create_container(container_name) # create a container in the storage account if it does not exist
        

    blob_items = container_client.list_blobs() # list all the blobs in the container

    # lọc ra các blob có phần mở rộng là .csv
    csv_blobs = [b for b in blob_items if b.name.endswith('.csv')]

    # lấy tên của các tệp CSV
    csv_files = [b.name for b in csv_blobs]
    return csv_files
def upload_To_BlobStorage(file_path,file_name,container_name):
    try:
        blob_service = BlobServiceClient.from_connection_string(connection_string)
        print(file_name)
        blob_client = blob_service.get_blob_client(container = container_name,blob = file_name)
        with open(file_path,"rb") as data:
            blob_client.upload_blob(data)
        print('uploaded'+file_name+"file")
        alert = '<div style="color: green;">File uploaded successfully</div>'
        # Xóa file tạm
        
        return alert
    except:
        alert = '<div style="color: red;">File upload Existed</div>'
        return alert
#*** Flask configuration


app = Flask(__name__)
 
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.getcwd() + '/static/uploads'
# RESULT_FOLDER = os.getcwd() + '/static/img_result/'
@app.route('/')

def index():
    img_html = load_photo()
    csv_file = load_file()
    return render_template('index.html',img_html = Markup(img_html),csv_file= csv_file)
 
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
        
        alert = upload_To_BlobStorage(file_path, filename,container_name='test1')

        os.remove(file_path)

        # Render template with active link
        img_html = load_photo()
        csv_file = load_file()

        return render_template('index.html', alert1=Markup(alert),img_html = Markup(img_html),csv_file= csv_file)
    return render_template('index.html', active_link='#home',img_html = Markup(img_html),csv_file= csv_file)

# định nghĩa một URL để tải xuống các tệp CSV
# @app.route('/download/<filename>')
# def download(filename):
#     blob_service_client = BlobServiceClient.from_connection_string(conn_str=connection_string)
#     container_name = 'test1'
#     container_client = blob_service_client.get_container_client(container=container_name)
#     blob_client = container_client.get_blob_client(filename)
#     file_content = blob_client.download_blob().content_as_text()
#     print('helooooo')
#     return Response(
#         file_content,
#         mimetype='text/csv',
#         headers={
#             "Content-disposition":
#             f"attachment; filename={filename}"
#         })

@app.route('/uploadphoto',  methods=("POST", "GET"))
def uploadPhoto():
    if request.method == 'POST':
       # session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)
        uploaded_file = request.files['photos']
        filename = secure_filename(uploaded_file.filename)

        # Lưu nội dung file upload vào file tạm
        uploaded_file.save(os.path.join(UPLOAD_FOLDER, filename))
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        # Gọi hàm upload file tới Blob Storage
        
        alert = upload_To_BlobStorage(file_path, filename,container_name='photos')

        # Xóa file tạm
        os.remove(file_path)
        img_html = load_photo()
        csv_file = load_file()

        # Render template with active link
        print(img_html)
        return render_template('index.html', active_link=Markup('home'), alert2=Markup(alert),img_html = Markup(img_html),csv_file= csv_file)
    # return render_template('index.html', active_link='#home',img_html = Markup(img_html))
if __name__=='__main__':
    app.run(host="0.0.0.0",port = 80)
