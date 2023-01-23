from app import app
from flask import render_template


@app.route('/new_trader', methods=['get'])
def new_trader():
    html = render_template(
        'new_trader.html',
    )
    return html
