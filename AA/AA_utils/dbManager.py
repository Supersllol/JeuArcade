import sqlite3
import os
from AA.AA_utils import settings
from AA.AA_game import player


class DatabasePlayerRecord:

    def __init__(self, playerName: str, playerCountry: str, win: int,
                 lose: int):
        self._playerName = playerName
        self._playerCountry = playerCountry
        self._win = int(win)
        self._lose = int(lose)

    @property
    def playerName(self):
        return self._playerName

    @property
    def playerCountry(self):
        return self._playerCountry

    @property
    def win(self):
        return self._win

    @property
    def lose(self):
        return self._lose


class DatabaseManager:

    def __init__(self):
        db_path = os.path.join(settings.PARENT_PATH, "record.db")
        self._db = sqlite3.connect(db_path)
        self._cursor = self._db.cursor()
        # use INTEGER for numeric columns
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS records(
                   nom TEXT NOT NULL,
                   country TEXT NOT NULL,
                   win INTEGER NOT NULL,
                   lose INTEGER NOT NULL
               )""")
        self._db.commit()

    def addPlayerResult(self, player: player.Player, win: bool):
        savedPlayers = self.getSavedPlayers()
        player_name = player._name
        if player_name in savedPlayers:
            # update existing record
            if win:
                new_win = savedPlayers[player_name].win + 1
                self._cursor.execute(
                    "UPDATE records SET win = ? WHERE nom = ?",
                    (new_win, player_name))
                self._db.commit()
            else:
                new_lose = savedPlayers[player_name].lose + 1
                self._cursor.execute(
                    "UPDATE records SET lose = ? WHERE nom = ?",
                    (new_lose, player_name))
                self._db.commit()
        else:
            # insert new record; store win/lose as integers (1/0)
            self._cursor.execute(
                "INSERT INTO records(nom, country, win, lose) VALUES (?, ?, ?, ?)",
                (player_name, player._country.name, int(win), int(not win)))
            self._db.commit()

    def getSavedPlayers(self):
        rows = self._cursor.execute(
            "SELECT nom, country, win, lose FROM records")
        return {
            row[0]: DatabasePlayerRecord(row[0], row[1], int(row[2]),
                                         int(row[3]))
            for row in rows
        }

    def deleteAll(self):
        # delete all rows from the records table
        self._cursor.execute("DELETE FROM records")
        self._db.commit()

    def getRecordOrder(self):
        """Return a list of DatabasePlayerRecord ordered by:
           1) wins (descending = more wins first)
           2) losses (ascending = fewer losses breaks ties)
        """
        players = self.getSavedPlayers()
        # key: (-wins, losses) -> sorts wins descending, losses ascending
        ordered = sorted(players.values(), key=lambda r: (-r.win, r.lose))
        return ordered

    def closeConnection(self):
        self._db.close()
