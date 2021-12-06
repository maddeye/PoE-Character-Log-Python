from sqlalchemy import Column, String, Integer

from POEClogDatabase.models import Base


class Character(Base):
    __tablename__ = "Characters"

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    account = Column(String)
    name = Column(String)
    league = Column(String)
    classId = Column(Integer)
    ascendancyClass = Column(Integer)
    className = Column(String)
    level = Column(Integer)
    experience = Column(Integer)
    passives = Column(String)
    items = Column(String)
    pob = Column(String)

    def __init__(
        self,
        account_name: str,
        name: str,
        league: str,
        classId: int,
        ascendancyClass: int,
        className: str,
        level: int,
        experience: str,
        passives: str,
        items: str,
        pob: str,
    ):
        self.account = account_name
        self.name = name
        self.league = league
        self.classId = classId
        self.ascendancyClass = ascendancyClass
        self.className = className
        self.level = level
        self.experience = experience
        self.passives = passives
        self.items = items
        self.pob = pob

    def __init__(self, account_name: str):
        self.account = account_name

    def info(self):
        return {
            "name": self.name,
            "league": self.league,
            "classId": self.classId,
            "className": self.className,
            "ascendancyClass": self.ascendancyClass,
            "level": self.level,
            "experience": self.experience,
            "passives": self.passives,
            "items": self.items,
            "pob": self.pob,
        }

    def from_dict(self, char: dict):
        self.name = char["name"]
        self.league = char["league"]
        self.classId = char["classId"]
        self.ascendancyClass = char["ascendancyClass"]
        self.className = char["class"]
        self.level = char["level"]
        self.experience = char["experience"]
        self.passives = char["passives"]
        self.items = char["items"]
        self.pob = char["pob"]
