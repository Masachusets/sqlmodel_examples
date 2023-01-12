from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship, create_engine, Session, select

DATABASE_URL = f"postgresql://admin:1111@localhost:5433/sqlmodel_db"


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: List["Hero"] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes")


engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_teams_and_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")
        hero_deadpond = Hero(name="Deadpond",
                             secret_name="Dive Wilson",
                             team=team_z_force)
        hero_rusty_man = Hero(name="Rusty-Man",
                              secret_name="Tommy Sharp",
                              age=48,
                              team=team_preventers)
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")

        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)

        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)
        print("Created hero:", hero_spider_boy)


def create_team_with_heroes():
     with Session(engine) as session:
        hero_black_lion = Hero(name="Black Lion",
                               secret_name="Trevor Challa",
                               age=35)
        hero_sure_e = Hero(name="Princess Sure-E", secret_name="Sure-E")
        team_wakaland = Team(name="Wakaland",
                             headquarters="Wakaland Capital City",
                             heroes=[hero_black_lion, hero_sure_e],
                             )

        session.add(team_wakaland)

        session.commit()

        session.refresh(team_wakaland)

        print("Team Wakaland:", team_wakaland)


def create_heroes_and_added_to_team():
    with Session(engine) as session:
        statement = select(Team).where(Team.name == "Preventers")
        team_preventers = session.exec(statement).first()
        hero_tarantula = Hero(name="Tarantula",
                              secret_name="Natalia Roman-on",
                              age=32)
        hero_weird = Hero(name="Dr. Weird",
                          secret_name="Steve Weird",
                          age=36)
        hero_cap = Hero(name="Captain North America",
                        secret_name="Esteban Rogelios",
                        age=93)

        team_preventers.heroes.append(hero_tarantula)
        team_preventers.heroes.append(hero_weird)
        team_preventers.heroes.append(hero_cap)

        session.commit()

        session.refresh(hero_tarantula)
        session.refresh(hero_weird)
        session.refresh(hero_cap)

        print("Preventers new heroes:",
              hero_tarantula,
              hero_weird,
              hero_cap, sep='\n')


def select_team_by_hero(hero_name: str = "Rusty-Man"):
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == hero_name)
        result = session.exec(statement)
        hero_rusty_man = result.one()

        # statement = select(Team).where(Team.id == hero_rusty_man.team_id)
        # result = session.exec(statement)
        # team = result.first()
        print("Rusty-Man's team:", hero_rusty_man.team)


def select_heroes_from_team(team_name: str = "Preventers"):
    with Session(engine) as session:
        statement = select(Team).where(Team.name == team_name)
        result = session.exec(statement)
        team_preventers = result.one()

        print("Preventers heroes:", *team_preventers.heroes, sep='\n')


def main():
    # create_db_and_tables()
    # create_teams_and_heroes()
    # create_team_with_heroes()
    # create_heroes_and_added_to_team()
    # select_team_by_hero()
    select_heroes_from_team()
    # update_heroes()
    # delete_heroes()


if __name__ == "__main__":
    main()
