import os
import sqlite3
from sqlite3 import Error

# DEFINED DATABASE DIRECTORY
database = "database/accettazione_referti_DDeSP.db"


def check_directory():
    # function to check the main directory status, if some directory is missing, create it
    directoryList = ['database', 'documenti_accettazione', 'documenti_referti']
    for directory in directoryList:
        if not os.path.exists(directory):
            os.makedirs(directory)


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


def insert_referto(referto):
    """
    Create a new accetazione into the accettazioni table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' REPLACE INTO referti(id,id_accettazione,id_campione,unita_operativa,data_prelievo,data_accettazione,rapporto_di_prova,descrizione_campione,operatore_prelievo_campione,data_inizio_analisi,data_fine_analisi,risultato,documento_referto)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) '''

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
                                    id text PRIMARY KEY,
                                    id_accettazione text NOT NULL,
                                    id_campione text NOT NULL,
                                    unita_operativa text NOT NULL,
                                    data_prelievo text NOT NULL,
                                    data_accettazione text NOT NULL,
                                    rapporto_di_prova text,
                                    descrizione_campione text NOT NULL,
                                    operatore_prelievo_campione text NOT NULL,
                                    data_inizio_analisi text,
                                    data_fine_analisi text,
                                    risultato text,
                                    documento_referto text,
                                    FOREIGN KEY (id_accettazione) REFERENCES accettazioni (id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create accettazioni table
        create_table(conn, sql_create_accettazioni_table)
        # create referti table
        create_table(conn, sql_create_referti_table)
    else:
        print("Error! cannot create the database connection.")


# def test_accettazione():
#     accettazione = ('ABC123', 'NEFROLOGIA', '22/10/2021', '23/10/2021', 'A123',
#                     'TAMPONE_CAPPA', 'ERNESTO SPARALESTO', 'ACCETTAZIONE_ABC123.pdf')
#     insert_accettazione(accettazione)


# if __name__ == '__main__':
#     generate_tables()
#     # test_accettazione()
