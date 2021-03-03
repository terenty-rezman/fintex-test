from flask import (Blueprint, request, abort, send_file, redirect)

import downloads_list as dw
import flask_db

bp = Blueprint("storage", __name__, url_prefix="/storage")

@bp.route('/<string:alias>', methods=('GET',))
def get_file(alias:str):
    if alias not in dw.aliases:
        abort(404)
    
    filepath = flask_db.query_file_path(alias)
    
    if filepath:
        return send_file(filepath, as_attachment=True)

    print('redirect')
    return redirect(dw.urls[alias])