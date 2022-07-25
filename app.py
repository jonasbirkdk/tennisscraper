
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
import dns.resolver
import json
from bson import json_util
import os
from dotenv import load_dotenv
from pymongo import MongoClient

dirname = os.path.dirname(__file__)

app = Flask(
    __name__,
    static_folder=os.path.join(dirname, "../frontend/build"),
    static_url_path="",
)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

load_dotenv()
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
new_client = MongoClient(os.getenv("mongo_uri"))
new_db = new_client['InterviewCoach']
new_collection = new_db["tennis"]

@app.route("/", methods=["GET"])
def start():
    cursor = new_collection.find({})
    json_docs = [json.dumps(doc, default=json_util.default) for doc in cursor]
    return jsonify(json_docs)

if __name__ == "__main__":
    app.run()