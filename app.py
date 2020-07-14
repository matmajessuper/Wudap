import json
from json import JSONDecodeError
from pathlib import Path

from flask import request
from werkzeug.datastructures import FileStorage
from flask_restplus import Resource, reqparse, abort

from models import BrowserHistory
from run import api, app, db
from schema import BrowserHistorySchema

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)


@api.route('/upload')
class Upload(Resource):
    @api.expect(upload_parser)
    def post(self):
        file = request.files.get('file')
        if file:
            content = {}
            try:
                content = json.loads(request.files.get('file').read())
            except JSONDecodeError:
                abort(400, 'Invalid json file')
            Path("./files").mkdir(parents=True, exist_ok=True)
            with open('./files/browserhistory.json', 'w') as out_file:
                json.dump(content, out_file)

            for history in content.get('Browser History'):
                row = BrowserHistory(
                    favicon_url=history.get('favicon_url'),
                    page_transition=history.get('page_transition'),
                    title=history.get('title'),
                    url=history.get('url'),
                    domain='/'.join(history.get('url').split('/')[:3]),
                    client_id=history.get('client_id'),
                    time_usec=history.get('time_usec'),
                )
                db.session.add(row)
            db.session.commit()

            domains = set(row.domain for row in BrowserHistory.query.filter(BrowserHistory.domain.isnot(None)))
            results = []
            for domain in domains:
                r = dict()
                r['site'] = domain
                r['count'] = BrowserHistory.query.filter_by(domain=domain).count()
                results.append(r)
            results = sorted(results, key=lambda k: k['count'], reverse=True)
            browser_history_schema = BrowserHistorySchema(many=True)
            return browser_history_schema.dump(results)

        abort(400, 'Json file required')


if __name__ == '__main__':
    app.run()
