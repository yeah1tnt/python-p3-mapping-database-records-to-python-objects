import sqlite3

CONN = sqlite3.connect('music.db')
CURSOR = CONN.cursor()

class Song:

    all = []

    def __init__(self, name, album):
        self.id = None
        self.name = name
        self.album = album

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                album TEXT
            )
        """

        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS songs
        """

        CURSOR.execute(sql)

    def save(self):
        sql = """
            INSERT INTO songs (name, album)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.album))

        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM songs").fetchone()[0]

    @classmethod
    def create(cls, name, album):
        song = Song(name, album)
        song.save()
        return song

    # new code goes here!
    @classmethod
    def new_from_db(cls,row):
        song = cls(row[1], row[2])
        song.id = row[0]
        return song
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM songs
        """

        all = CURSOR.execute(sql).fetchall()
        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM songs
            WHERE name = ?
            LIMIT 1
        """
        song = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(song)