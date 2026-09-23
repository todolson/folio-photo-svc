import re

import requests
import yaml
from flask import Flask, Response, abort

app = Flask(__name__)

with open("config.yaml") as f:
    _cfg = yaml.safe_load(f)

_BASE_URL = _cfg["photo_api"]["base_url"]
_PATH = _cfg["photo_api"]["path"]
_AUTH = (_cfg["photo_api"]["username"], _cfg["photo_api"]["password"])

_ID_RE = re.compile(r"^[A-Za-z0-9]+$")


@app.route("/folio-photo/<id>")
def get_photo(id):
    if not _ID_RE.match(id):
        abort(400)
    url = f"{_BASE_URL}{_PATH}/{id}"
    try:
        resp = requests.get(url, auth=_AUTH, params={"inline": "true"}, timeout=10)
    except requests.RequestException:
        abort(502)
    if resp.status_code != 200:
        abort(resp.status_code)
    content_type = resp.headers.get("Content-Type", "image/jpeg")
    return Response(resp.content, content_type=content_type)
