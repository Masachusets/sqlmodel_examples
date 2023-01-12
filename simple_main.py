from typing import Optional

from sqlmodel import SQLModel, Field, create_engine, Session, select

DATABASE_URL = f"postgresql://admin:1111@localhost:5433/sqlmodel_db"


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str


engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_teams():
    team_1 = Team(name="Preventers", headquarters="Sharp Tower")
    team_2 = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

    with Session(engine) as session:
        session.add(team_1)
        session.add(team_2)

        session.commit()


def create_heroes():
    hero_1 = Hero(name="Deadpond",
                  secret_name="Dive Wilson",
                  team_id=2)
    hero_2 = Hero(name="Rusty-Man",
                  secret_name="Tommy Sharp",
                  age=48,
                  team_id=1)
    hero_3 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.add(hero_4)
        session.add(hero_5)
        session.add(hero_6)
        session.add(hero_7)

        session.commit()


def select_heroes_old():
    with Session(engine) as session:
        statement = select(Hero)
        results = session.exec(statement)
        heroes = results.all()
        print("Heroes:", *heroes, sep='\n')


def select_heroes():
    with Session(engine) as session:
        # statement = select(Hero, Team).where(Hero.team_id == Team.id)
        statement = select(Hero, Team).join(Team, isouter=True)
        results = session.exec(statement)
        heroes = results.all()
        print("Heroes:", *heroes, sep='\n')


def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero = results.one()
        print("Hero:", hero)

        # hero.team_id = 1
        hero.team_id = None
        session.add(hero)
        session.commit()
        session.refresh(hero)
        print('Updated hero', hero)


def delete_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero = results.one()
        print("Hero: ", hero)

        session.delete(hero)
        session.commit()
        print(f'Hero {hero} deleted')


def main():
    # create_db_and_tables()
    # create_teams()
    # create_heroes()
    select_heroes()
    # update_heroes()
    # delete_heroes()


if __name__ == "__main__":
    main()
