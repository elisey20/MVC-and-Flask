import pandas as pd


def all_stocks(conn):
    return pd.read_sql(f'''
        select 
            stock.stock_id as ID,
            name as Название,
            price as Цена,
            currency as Валюта,
            description as Описание
        from
            stock
            left join stock_price sp on stock.stock_id = sp.stock_id
    ''', conn)


def my_stocks(conn, account_id):
    return pd.read_sql(f'''
        select 
            stock.stock_id as ID,
            name as Название,
            sum(case
                when t.operation_type = 'buy'
                    then 1
                    else -1
                end) as Количество,
            sp.price as Цена,
            description as Описание
        from transactions t
            join stock on stock.stock_id = t.stock_id
            join stock_price sp on stock.stock_id = sp.stock_id
        where 
            t.account_id = {account_id}
        group by 
            stock.name
    ''', conn)
