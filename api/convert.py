import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # add project root

from prompt_to_xml.converter import convert_to_xml
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route("/api/convert", methods=["POST"])
def convert():
    data = request.get_json()
    prompt = data.get("prompt", "")
    xml_output = convert_to_xml(prompt)
    return jsonify({"xml": xml_output})

if __name__ == "__main__":
    app.run(debug=True)
