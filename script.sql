pragma foreign_keys = on;

create table if not exists account
(
    account_id integer primary key autoincrement,
    name       varchar(255),
    currency   varchar(4)
);

create table if not exists story_balance
(
    story_balance_id integer primary key autoincrement,
    account_id       integer,
    operation_type   varchar(4),
    amount           double,
    foreign key (account_id) references account (account_id)
        on delete cascade on update cascade
);

create table if not exists stock
(
    stock_id    integer primary key autoincrement,
    name        varchar(255),
    currency    varchar(4),
    description text
);

create table if not exists stock_price
(
    stock_price_id integer primary key autoincrement,
    stock_id       integer,
    date           timestamptz,
    price          double,
    foreign key (stock_id) references stock (stock_id)
        on delete cascade on update cascade
);

create table if not exists transactions
(
    transaction_id    integer primary key autoincrement,
    account_id        integer,
    stock_id          integer,
    operation_type    varchar(4),
    transaction_price double,
    date_time         timestamptz,
    foreign key (account_id) references account (account_id)
        on delete cascade on update cascade,
    foreign key (stock_id) references stock (stock_id)
        on delete cascade on update cascade
);

insert into stock (name, currency, description)
VALUES ('ГлобалТранс (GLTRDR)', 'RUB',
        'Глобалтранс Инвестментс является кипрской холдинговой компанией. Основными видами деятельности Компании является предоставление железнодорожных транспортных услуг с использованием собственного или арендованного подвижного состава или поездов сторонних железнодорожных операторов, а также операционная аренда подвижного состава и услуги по экспедированию грузов (агентские услуги).');
insert into stock (name, currency, description)
VALUES ('HeadHunter Group PLC ADR (HHRUDR)', 'RUB',
        'Хэдхантер Груп Пиэлси является кипрской компанией, которая управляет платформой онлайн-найма. Компания предоставляет ряд услуг работодателям и рекрутерам, включая доступ к базе данных биографических данных.');
insert into stock (name, currency, description)
VALUES ('Ozon Holdings PLC (OZONDR)', 'RUB',
        'Озон Холдингс Лимитед является платформой электронной коммерции в России. Компания связывает и облегчает сделки между покупателями и продавцами. Компания также продает продукцию напрямую своим покупателям. Компания предоставляет две платформы Ozon.ru и Ozon.travel.');
insert into stock (name, currency, description)
VALUES ('ОАО Аэрофлот (AFLT)', 'RUB',
        'ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО "АЭРОФЛОТ-РОССИЙСКИЕ АВИАЛИНИИ" является российской компанией, которая предоставляет услуги в области пассажирских и грузовых перевозок и выполняет как внутренние, так и международные рейсы. Компания и ее дочерние предприятия также предоставляют услуги по бортовому питанию и страхованию.');
insert into stock (name, currency, description)
VALUES ('ВТБ RTS ПАО (VTBR)', 'RUB',
        'БАНК ВТБ (ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО) является российским коммерческим банком. Банк выделил пять отчетных сегментов: Корпоративно-инвестиционный бизнес ориентирован на обслуживание юридических лиц, относящихся к категории «крупный бизнес» и проведение операций с банковскими финансовыми организациями, а также на проведение операций на рынках ценных бумаг.');
insert into stock (name, currency, description)
VALUES ('Газпром ПАО (GAZP)', 'RUB',
        'Публичное акционерное общество "Газпром" является компанией, которая управляет газопроводными системами. Основными видами деятельности Компании являются разведка месторождений и добыча газа; транспортировка газа; продажа газа на территории Российской Федерации и за рубежом; хранение газа; добыча сырой нефти и газового конденсата; переработка нефти, газового конденсата и прочих углеводородов, а также продажа продуктов переработки, электрической и тепловой энергии.');

insert into stock_price (stock_id, date, price)
values (1, date(), 12);
insert into stock_price (stock_id, date, price)
values (2, date(), 45);
insert into stock_price (stock_id, date, price)
values (3, date(), 109);
insert into stock_price (stock_id, date, price)
values (4, date(), 74);
insert into stock_price (stock_id, date, price)
values (5, date(), 21);
insert into stock_price (stock_id, date, price)
values (6, date(), 456);

insert into account (name, currency)
values ('Елисей', 'RUB');
insert into account (name, currency)
values ('Никита', 'RUB');
insert into account (name, currency)
values ('Борис', 'RUB');

insert into transactions (account_id, stock_id, operation_type, transaction_price, date_time)
values (1, 1, 'buy', 69.24, time());

insert into stock_price (stock_id, date, price)
values (1, date(), 69);
