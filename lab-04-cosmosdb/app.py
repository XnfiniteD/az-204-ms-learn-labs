import os
import flask
from flask import request, jsonify
from services.app_service import AppService
from azure.cosmos import CosmosClient

cosmosDbConnectionString = os.environ.get('COSMOS_CONNECTION_STRING')
cosmosDatabase = os.environ.get('COSMOS_DATABASE')
blobConnectionString = os.environ.get('BLOB_CONNECTION_STRING')

app = flask.Flask(__name__)
appService = AppService(cosmosDbConnectionString, cosmosDatabase, blobConnectionString)

@app.route('/')
def main():
    containers = [container.name for container in appService.get_all_blob_containers()]
    
    return flask.render_template('index.html', data={
        'containers': containers
    })

@app.route('/upload', methods=['POST'])
def upload_media():
    payload = request.form
    appService.upload_media_file()


@app.route('/get_blobs', methods=['GET'])
def get_blobs():
    container = request.args.get('contaner')
    metadata = []
    for blob in appService.get_container_blobs(container):
        metadata.append(blob)
    return jsonify({
        'status': 200,
        'blobs': metadata
    })

if __name__ == "__main__":
    app.run(debug=True)