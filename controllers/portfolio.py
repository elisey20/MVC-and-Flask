from app import app
from flask import render_template, request, session, redirect
from utils import get_db_connection
from models.index_model import get_account, get_stock_client, get_new_account, buy_stock, \
    sell_stock, get_portfolio_cost, update_stock_prices


@app.route('/', methods=['get'])
def index():
    return redirect('/portfolio')


@app.route('/portfolio', methods=['get'])
def portfolio():
    conn = get_db_connection()
    update_stock_prices(conn)

    if request.values.get('account'):
        account_id = int(request.values.get('account'))
        session['account_id'] = account_id
    elif request.values.get('new_trader'):
        new_account = request.values.get('new_trader')
        session['account_id'] = get_new_account(conn, new_account)
    elif request.values.get('buy_stock'):
        stock_id = int(request.values.get('buy_stock'))
        buy_stock(conn, stock_id, session['account_id'])
    elif request.values.get('sell_stock'):
        stock_id = int(request.values.get('sell_stock'))
        sell_stock(conn, stock_id, session['account_id'])
    else:
        session['account_id'] = 1

    df_account = get_account(conn)
    df_stock_client = get_stock_client(conn, session['account_id'])
    portfolio_cost = get_portfolio_cost(conn, session['account_id'])

    # выводим форму
    html = render_template(
        'portfolio.html',
        account_id=session['account_id'],
        combo_box=df_account,
        stock_client=df_stock_client,
        portfolio_cost=portfolio_cost,
        len=len
    )
    return html
