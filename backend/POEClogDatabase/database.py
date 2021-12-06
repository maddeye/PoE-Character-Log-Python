from contextlib import contextmanager
from logging import Logger
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker


from POEClogDatabase.models import Base, Character


class Database:
    def __init__(self, logger: Logger, uri="sqlite:///data/poeclog.db"):
        """Initialize sql connection"""
        self.logger = logger

        self.engine = create_engine(uri)
        self.SessionMaker = sessionmaker(bind=self.engine)

    @contextmanager
    def db_session(self):
        """
        Creates a context with an open SQLAlchemy session.
        """
        session: Session = scoped_session(self.SessionMaker)
        yield session
        session.commit()
        session.close()

    def get_char(self, character_name: str) -> Character:
        """
        Return latest character information
        """
        session: Session

        with self.db_session() as session:
            char: Character = (
                session.query(Character)
                .filter(Character.name == character_name)
                .first()
            )
            
            session.expunge_all()

            return char

    def get_char_with_level(self, character_name: str, level: int) -> Character:
        """
        Return latest character information
        """
        session: Session

        with self.db_session() as session:
            char: Character = (
                session.query(Character)
                .filter(Character.name == character_name, Character.level == level)
                .first()
            )
            
            session.expunge_all()

            return char

    def get_all(self) -> List[Character]:
        """
        Get all characters
        """
        session: Session

        with self.db_session() as session:
            chars = session.query(Character).all()
            
            session.expunge_all()
            return chars

    def get_history(self, character_name: str) -> List[Character]:
        """Get history of character"""
        session: Session

        with self.db_session() as session:
            history: List[Character] = (
                session.query(Character).filter(Character.name == character_name).all()
            )
            
            session.expunge_all()

            return history

    def store_char(self, account_name: str, character: dict):
        session: Session

        char: Character = Character(account_name)
        char.from_dict(character)
        with self.db_session() as session:
            if not self.get_char_with_level(char.name, char.level):
                session.add(char)
                session.commit()

    def create_database(self):
        Base.metadata.create_all(self.engine)


if __name__ == "__main__":
    db = Database(Logger())
    db.create_database()
