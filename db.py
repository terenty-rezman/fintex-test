import os
import sqlite3
import click

DATABASE = os.path.join(".", 'db.sqlite')


def get_db():
    db = sqlite3.connect(
        DATABASE,
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row

    return db


def close_db(db):
    db.close()


class db_connection:
    def __init__(self):
        self.db = None

    def __enter__(self):
        self.db = get_db()
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        close_db(self.db)

        if exc_type:
            return False

        return True


def query_file_path(alias: str):
    with db_connection() as db:
        return _query_file_path(db, alias)


def _query_file_path(db, alias: str):
    file = db.execute(
        'SELECT * FROM downloads WHERE alias = ?', (alias,)
    ).fetchone()

    if file:
        return file["path"]

    return None


def update_file_path(alias: str, path: str):
    with db_connection() as db:
        return _update_file_path(db, alias, path)


def _update_file_path(db, alias: str, path: str):
    if db.execute(
        'SELECT * FROM downloads WHERE alias = ?', (alias,)
    ).fetchone() is None:
        db.execute(
            'INSERT INTO downloads (alias, path) VALUES (?, ?)',
            (alias, path)
        )
    else:
        db.execute(
            'UPDATE downloads SET path = ? WHERE alias = ?',
            (path, alias)
        )

    db.commit()


@click.group()
def cli():
    pass


@cli.command("initdb")
def init_db_command():
    """Clear existing SQL db data and recreate tables."""
    with db_connection() as db:
        with open('schema.sql') as f:
            db.executescript(f.read())
            print("db recreated")


if __name__ == "__main__":
    cli()
