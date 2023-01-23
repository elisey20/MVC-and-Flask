from app import app
from flask import render_template
from utils import get_db_connection
from models.search_model import all_stocks


@app.route('/buy', methods=['get', 'post'])
def buy():
    conn = get_db_connection()

    df_card = all_stocks(conn)

    html = render_template(
        'buy.html',
        card=df_card,
        len=len
    )
    return html
