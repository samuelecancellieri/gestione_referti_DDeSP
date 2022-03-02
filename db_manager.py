import sqlite3
from sqlite3 import Error
from traceback import print_tb
import pandas as pd

# DEFINED DATABASE DIRECTORY
database = "database/accettazione_referti_DDeSP.db"


def delete_record_identificazione(id_accettazione, id_campione):
    """
    Delete a record in referti_identificazione by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute(f"DELETE from referti_identificazione WHERE id_accettazione=? AND id_campione=?",
                (id_accettazione, id_campione))
    conn.commit()
    conn.close()

    return True


def get_id_last_row(table_to_query):
    conn = sqlite3.connect(database)
    tabella = pd.read_sql_query(
        f"SELECT * FROM {table_to_query}", conn)
    conn.commit()
    conn.close()
    if len(tabella.index) == 0:
        return 0
    tabella.reset_index(inplace=True)
    tabella['index'] += 1
    # print(tabella)
    return tabella['index'].max()


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_identificazione(referto):
    sql = ''' REPLACE INTO referti_identificazione(rapporto_di_prova_identificazione,
id_accettazione,
id_campione,
unita_operativa,
data_prelievo,
data_accettazione,
descrizione_campione,
operatore_prelievo_campione,
operatore_analisi,
data_inizio_analisi,
data_fine_analisi,
identificazione,
note,
documento_identificazione)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''

    conn = create_connection(database)

    cur = conn.cursor()
    cur.execute(sql, referto)
    conn.commit()
    return cur.lastrowid


def insert_referto(referto):
    """
    Create a new accetazione into the accettazioni table
    :param conn:
    :param project:
    :return: project id
    """

    sql = ''' REPLACE INTO referti(rapporto_di_prova,id_accettazione,id_campione,
    unita_operativa,data_prelievo,data_accettazione,
    descrizione_campione,operatore_prelievo_campione,
    operatore_analisi,data_inizio_analisi,data_fine_analisi,
    UFC_batteri,UFC_miceti,note,documento_referto)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''

    conn = create_connection(database)

    cur = conn.cursor()
    cur.execute(sql, referto)
    conn.commit()
    return cur.lastrowid


def insert_accettazione(accettazione):
    """
    Create a new accetazione into the accettazioni table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' REPLACE INTO accettazioni(id,unita_operativa,data_prelievo,data_accettazione,id_campioni,descrizione_campioni,operatore_prelievo_campioni,documento_accettazione)
              VALUES(?,?,?,?,?,?,?,?) '''

    conn = create_connection(database)

    cur = conn.cursor()
    cur.execute(sql, accettazione)
    conn.commit()
    return cur.lastrowid


def generate_tables():
    sql_create_accettazioni_table = """ CREATE TABLE IF NOT EXISTS accettazioni (
                                        id text PRIMARY KEY,
                                        unita_operativa text NOT NULL,
                                        data_prelievo text NOT NULL,
                                        data_accettazione text NOT NULL,
                                        id_campioni text NOT NULL,
                                        descrizione_campioni text NOT NULL,
                                        operatore_prelievo_campioni text NOT NULL,
                                        documento_accettazione text NOT NULL
                                    ); """

    sql_create_referti_table = """CREATE TABLE IF NOT EXISTS referti (
                                    rapporto_di_prova text PRIMARY KEY,
                                    id_accettazione text NOT NULL,
                                    id_campione text NOT NULL,
                                    unita_operativa text NOT NULL,
                                    data_prelievo text NOT NULL,
                                    data_accettazione text NOT NULL,
                                    descrizione_campione text NOT NULL,
                                    operatore_prelievo_campione text NOT NULL,
                                    operatore_analisi text NOT NULL,
                                    data_inizio_analisi text,
                                    data_fine_analisi text,
                                    UFC_batteri text,
                                    UFC_miceti text,
                                    note text,
                                    documento_referto text,
                                    FOREIGN KEY (id_accettazione) REFERENCES accettazioni (id)
                                );"""

    sql_create_referti_identificazione_table = """CREATE TABLE IF NOT EXISTS referti_identificazione (
                                    rapporto_di_prova_identificazione text PRIMARY KEY,
                                    id_accettazione text NOT NULL,
                                    id_campione text NOT NULL,
                                    unita_operativa text NOT NULL,
                                    data_prelievo text NOT NULL,
                                    data_accettazione text NOT NULL,
                                    descrizione_campione text NOT NULL,
                                    operatore_prelievo_campione text NOT NULL,
                                    operatore_analisi text NOT NULL,
                                    data_inizio_analisi text,
                                    data_fine_analisi text,
                                    identificazione text,
                                    note text,
                                    documento_identificazione text,
                                    FOREIGN KEY (id_accettazione) REFERENCES accettazioni (id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn:
        # create accettazioni table
        create_table(conn, sql_create_accettazioni_table)
        # create referti table
        create_table(conn, sql_create_referti_table)
        # create identificazione table
        create_table(conn, sql_create_referti_identificazione_table)
    else:
        print("Error! cannot create the database connection.")
