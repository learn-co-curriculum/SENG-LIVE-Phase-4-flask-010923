#!/usr/bin/env python3
from app import app
from models import db, Production
# Note: This or flask shell can be used to query data. If flask shell is used remember to import app and the models
# 11.✅ Run some queries to review SQLAlchemy and verify your Database. An example is listed bellow but feel free to play around with additional queries. Run exit() when done.
    # run python debug.py
    # ipdb> with app.app_context():
    #   Production.query.all()
# 12.✅ navigate to app.py
if __name__ == '__main__':
    import ipdb; ipdb.set_trace()
