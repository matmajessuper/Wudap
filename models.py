from run import db


class BrowserHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favicon_url = db.Column(db.Text, nullable=True)
    page_transition = db.Column(db.String(50), nullable=True)
    title = db.Column(db.String(50), nullable=True)
    url = db.Column(db.Text, nullable=True)
    domain = db.Column(db.Text, nullable=True)
    client_id = db.Column(db.String(50), nullable=True)
    time_usec = db.Column(db.BIGINT, nullable=True)
