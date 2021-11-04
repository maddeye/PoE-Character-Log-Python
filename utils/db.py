import sqlite3

from typing import List


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DB:
    def __init__(self, db_path: str):
        """Create a database connection and creates one if database does not already exist"""
        self.con = sqlite3.connect(db_path)
        self.con.row_factory = dict_factory

        self.cursor = self.con.cursor()

    def store_character(self, character: dict):
        self._check_for_table()

        if self._check_if_already_exist(character["name"], character["level"]):
            return False

        sql = "INSERT INTO 'Characters' VALUES (:name, :league, :classId, :ascendancyClass, :class, :level, :experience, :passives, :items, :pob)"
        self.cursor.execute(sql, character)

    def get_char(self, character_name: str) -> dict:
        self._check_for_table()

        sql = "SELECT * FROM 'Characters' WHERE name = ?"
        self.cursor.execute(sql, [character_name])

        return self.cursor.fetchone()

    def get_all(self) -> List[dict]:
        sql = "SELECT * FROM 'Characters'"
        self.cursor.execute(sql)

        return self.cursor.fetchall()

    def get_history(self, character_name: str) -> List[dict]:
        sql = "SELECT * FROM 'Characters' WHERE name = ?"
        self.cursor.execute(sql, [character_name])

        return self.cursor.fetchall()

    def close(self):
        self.con.commit()
        self.con.close()

    def _check_for_table(self):
        sql = "CREATE TABLE IF NOT EXISTS 'Characters' (name TEXT, league TEXT, classId NUMBER, ascendancyClass NUMBER, class TEXT, level NUMBER, experience NUMBER, passives TEXT, items TEXT, pob TEXT);"
        self.cursor.execute(sql)

    def _check_if_already_exist(self, character_name: str, level: int) -> bool:
        sql = "SELECT * from 'Characters' WHERE name = ? AND level = ?"
        self.cursor.execute(sql, [character_name, level])

        if self.cursor.fetchone():
            return True

        return False
