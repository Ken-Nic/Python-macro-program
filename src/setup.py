import sqlite3


# Create database to house macro data
def setup_db():
    conn = sqlite3.connect('macro_database.db')
    c = conn.cursor()

    # Clean up any old tables that maybe around
    c.execute("""DROP TABLE IF EXISTS MacroGroups""")
    c.execute("""DROP TABLE IF EXISTS MacroRecords""")
    conn.commit()

    # Table for macro groups
    c.execute("""CREATE TABLE MacroGroups (
        Id INTEGER PRIMARY KEY NOT NULL,
        Name VARCHAR(25) NOT NULL
        )""")

    # Table for individual macros or macroRecords
    c.execute("""CREATE TABLE MacroRecords (
        Id INTEGER PRIMARY KEY NOT NULL,
        Name VARCHAR(50) NOT NULL,
        GroupID INTEGER NOT NULL,
        Type VARCHAR(1) NOT NULL,
        Address STRING NOT NULL,
        FOREIGN KEY(GroupID) REFERENCES MacroGroups(Id)
        )""")

    conn.commit()
    conn.close()


if __name__ == '__main__' :
    setup_db()
