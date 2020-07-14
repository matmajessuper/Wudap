import json
from collections import Counter
from json import JSONDecodeError
from pathlib import Path

from flask import request
from werkzeug.datastructures import FileStorage
from flask_restplus import Resource, reqparse, abort

from run import api, app
from schema import BrowserHistorySchema

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)


@api.route('/upload')
class Upload(Resource):
    @api.expect(upload_parser)
    def post(self):
        file = request.files.get('file')
        if not file:
            abort(400, 'Json file required')

        content = {}
        try:
            content = json.loads(request.files.get('file').read())
        except JSONDecodeError:
            abort(400, 'Invalid json file')
        Path("./files").mkdir(parents=True, exist_ok=True)
        with open('./files/browserhistory.json', 'w') as out_file:
            json.dump(content, out_file)

        browser_history = content.get('Browser History')
        for i, history in enumerate(browser_history):
            browser_history[i]['domain'] = '/'.join(history.get('url').split('/')[:3])

        counters = dict(Counter(r.get('domain') for r in browser_history))
        results = []
        for k, v in counters.items():
            row = dict()
            row['site'] = k
            row['count'] = v
            results.append(row)

        results = sorted(results, key=lambda k: k['count'], reverse=True)
        browser_history_schema = BrowserHistorySchema(many=True)
        return browser_history_schema.dump(results)



if __name__ == '__main__':
    app.run()
