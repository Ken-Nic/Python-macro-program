import sqlite3
from sqlite3 import OperationalError
from setup import setup_db


class DatabaseAccess:
    def __init__(self, db_name):
        self.conn = sqlite3.connect("macro_database.db")
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def check_db(self):
        try:
            self.c.execute("SELECT * FROM MacroGroups")
            self.conn.commit()
            return True
        except OperationalError:
            setup_db()
            return True

    def check_group_by_name(self, name):
        self.c.execute(f"SELECT * FROM MacroGroups WHERE Name = '{name}'")
        self.conn.commit()
        db_results = self.c.fetchall()
        if len(db_results) == 0:
            return False
        else:
            return True

    def check_group_by_Id(self, Id):
        self.c.execute(f"SELECT * FROM MacroGroups WHERE Id = '{Id}'")
        self.conn.commit()
        db_results = self.c.fetchall()
        if len(db_results) == 0:
            return False
        else:
            return True

    def find_group_name(self,id):
        self.c.execute(f"SELECT Name FROM MacroGroups WHERE Id ='{id}'")
        self.conn.commit()
        db_results = self.c.fetchall()
        return db_results[0]

    def add_group(self, name):
        if self.check_group_by_name(name) is False:
            command = f"INSERT INTO MacroGroups (Name) VALUES ('{name}');"
            self.c.execute(command)
            self.conn.commit()
            return 0
        else:
            return 1

    def delete_group(self,Id):
        if self.check_group_by_Id(Id) is True:
            command = f"DELETE FROM MacroGroups WHERE Id = '{Id}';"
            self.c.execute(command)
            command = f"DELETE FROM MacroRecords WHERE GroupID = '{Id}';"
            self.c.execute(command)
            self.conn.commit()

    def edit_group_name(self,Id,new_name):
        if self.check_group_by_Id(Id) is True:
            command = f"UPDATE MacroGroups SET Name='{new_name}' WHERE Id={Id}"
            self.c.execute(command)
            self.conn.commit()

    def get_groups(self):
        self.c.execute("SELECT * FROM MacroGroups")
        self.conn.commit()

        db_results = self.c.fetchall()
        return db_results

    def add_record(self, name,group_id, type, address):
        command = f"INSERT INTO MacroRecords (Name,GroupID,Type,Address) VALUES ('{name}',{group_id},'{type}','{address}');"
        self.c.execute(command)
        self.conn.commit()

    def delete_record(self, id, groupId):
        command = f"DELETE FROM MacroRecords WHERE Id = '{id}' AND GroupID = '{groupId}'"
        self.c.execute(command)
        self.conn.commit()

    def get_all_records(self, groupId):
        self.c.execute(f"SELECT * FROM MacroRecords WHERE groupId = {groupId}")
        self.conn.commit()

        db_results = self.c.fetchall()
        return db_results

    def get_record(self, id, groupId):
        self.c.execute(f"SELECT * FROM MacroRecords WHERE groupId = {groupId} AND id = {id}")
        self.conn.commit()

        db_results = self.c.fetchall()
        return db_results

    def edit_record_address(self, id, groupId, address):
        self.c.execute(f"UPDATE MacroRecords SET address='{address}' WHERE Id = {id} AND groupId = {groupId}")
        self.conn.commit()

    def edit_record_name(self, id, groupId, name):
        self.c.execute(f"UPDATE MacroRecords SET Name='{name}' WHERE Id = {id} AND groupId = {groupId}")
        self.conn.commit()

    def check_record(self, group_id, address):
        self.c.execute(f"SELECT * FROM MacroRecords WHERE groupId={group_id} AND Address='{address}'")
        self.conn.commit()
        db_results = self.c.fetchall()
        if len(db_results) == 0:
            return False
        else:
            return True

    def get_records_by_type(self, type, group_id):
        self.c.execute(f"SELECT * FROM MacroRecords WHERE Type='{type}' AND groupId = {group_id}")
        self.conn.commit()
        db_results = self.c.fetchall()
        return db_results