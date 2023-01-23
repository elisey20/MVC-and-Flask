from random import Random
import pandas
from .search_model import all_stocks


def get_account(conn):
    return pandas.read_sql(
        '''SELECT * FROM account
''', conn)


def get_stock_client(conn, account_id):
    return pandas.read_sql('''
            select 
                s.name as Название,
                a.currency as Валюта,
                sum(case
                    when t.operation_type = 'buy'
                        then 1
                        else -1
                    end) as Количество,
                round(avg(t.transaction_price), 3) as 'Цена покупки',
                s.description as Описание
            from stock s
                join transactions t on s.stock_id = t.stock_id
                join account a on t.account_id = a.account_id
            where 
                a.account_id = :id
            group by 
                t.stock_id
         ''', conn, params={"id": account_id})


def get_portfolio_cost(conn, account_id):
    buying_count_data = get_buying_count(conn, account_id)
    buying_count = 1 if buying_count_data.dropna().empty else buying_count_data.loc[0, 'count']

    selling_count_data = get_selling_count(conn, account_id)
    selling_count = 0 if selling_count_data.dropna().empty else selling_count_data.loc[0, 'count']

    avg_buying_data = get_avg_buying(conn, account_id)
    avg_buying = 1 if avg_buying_data.dropna().empty else avg_buying_data.loc[0, 'avg']

    avg_selling_data = get_avg_selling(conn, account_id)
    avg_selling = 0 if avg_selling_data.dropna().empty else avg_selling_data.loc[0, 'avg']

    return '{:.3f}'.format(buying_count * avg_buying - selling_count * avg_selling)


def get_buying_count(conn, account_id):
    return pandas.read_sql(f'''
                select 
                    count(t.transaction_id) as count
                from transactions t
                    join account a on t.account_id = a.account_id
                where 
                    a.account_id = {account_id} and
                    t.operation_type = 'buy'
             ''', conn)


def get_selling_count(conn, account_id):
    return pandas.read_sql(f'''
                select 
                    count(t.operation_type) as count
                from transactions t
                    join account a on t.account_id = a.account_id
                where 
                    a.account_id = {account_id} and
                    t.operation_type = 'sell'
             ''', conn)


def get_avg_buying(conn, account_id):
    return pandas.read_sql(f'''
                select 
                    avg(t.transaction_price) as avg
                from transactions t
                    join account a on t.account_id = a.account_id
                where 
                    a.account_id = {account_id} and
                    t.operation_type = 'buy'
             ''', conn)


def get_avg_selling(conn, account_id):
    return pandas.read_sql(f'''
                select 
                    avg(t.transaction_price) as avg
                from transactions t
                    join account a on t.account_id = a.account_id
                where 
                    a.account_id = {account_id} and
                    t.operation_type = 'sell'
             ''', conn)


def get_new_account(conn, new_account):
    cur = conn.cursor()

    cur.execute('''
        INSERT INTO account (name, currency) VALUES (:new_account, 'RUB')
    ''', {"new_account": new_account})

    conn.commit()

    return cur.lastrowid


def buy_stock(conn, stock_id, account_id) -> None:
    frame = get_stock_price(conn, stock_id)
    price = 0 if frame.dropna().empty else frame.loc[0, 'price']

    cur = conn.cursor()

    cur.executescript(f'''
INSERT INTO transactions 
    (account_id, stock_id, operation_type, transaction_price, date_time) 
VALUES 
    ({account_id}, {stock_id}, 'buy', {price}, time());
    ''')

    return conn.commit()


def sell_stock(conn, stock_id, account_id) -> None:
    frame = get_stock_price(conn, stock_id)
    price = 0 if frame.dropna().empty else frame.loc[0, 'price']

    cur = conn.cursor()

    cur.executescript(f'''
INSERT INTO transactions 
    (account_id, stock_id, operation_type, transaction_price, date_time) 
VALUES 
    ({account_id}, {stock_id}, 'sell', {price}, time());
    ''')

    return conn.commit()


def get_stock_price(conn, stock_id):
    return pandas.read_sql(f'''
        select
            price
        from stock
            join stock_price sp on stock.stock_id = sp.stock_id
        where 
            stock.stock_id = {stock_id}
        ''', conn)


def update_stock_prices(conn):
    cur = conn.cursor()
    stocks = all_stocks(conn)
    n = len(stocks)
    rand = Random()
    for i in range(n):
        price = stocks.loc[i, 'Цена']
        new_price = price + rand.random() * 2 - 1
        cur.executescript(f'''
            update 
                stock_price
            set 
                price = round({new_price}, 3)
            where
                stock_price_id = {i+1}
            ''')
        conn.commit()


