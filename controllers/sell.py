from app import app
from flask import render_template, session
from utils import get_db_connection
from models.search_model import my_stocks


@app.route('/sell', methods=['get', 'post'])
def sell():
    conn = get_db_connection()

    df_card = my_stocks(conn, session['account_id'])

    html = render_template(
        'sell.html',
        card=df_card,
        len=len
    )
    return html
