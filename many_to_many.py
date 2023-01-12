from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship, create_engine, Session, select

DATABASE_URL = f"postgresql://admin:1111@localhost:5433/sqlmodel_db"


class HeroTeamLink(SQLModel, table=True):
    team_id: Optional[int] = Field(default=None,
                                   foreign_key="team.id",
                                   primary_key=True
                                   )
    hero_id: Optional[int] = Field(default=None,
                                   foreign_key="hero.id",
                                   primary_key=True
                                   )


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: List["Hero"] = Relationship(back_populates="teams",
                                        link_model=HeroTeamLink)


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    teams: List[Team] = Relationship(back_populates="heroes",
                                     link_model=HeroTeamLink)


engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_teams_and_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret’s Bar")

        hero_deadpond = Hero(
            name="Deadpond",
            secret_name="Dive Wilson",
            teams=[team_z_force, team_preventers],
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            teams=[team_preventers],
        )
        hero_spider_boy = Hero(
            name="Spider-Boy",
            secret_name="Pedro Parqueador",
            teams=[team_preventers]
        )
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Deadpond:", hero_deadpond, hero_deadpond.teams, sep='\n')
        print("Rusty-Man:", hero_rusty_man, hero_rusty_man.teams, sep='\n')
        print("Spider-Boy:", hero_spider_boy, hero_spider_boy.teams, sep='\n')


def update_teams():
    with Session(engine) as session:
        hero_spider_boy = session.exec(
            select(Hero).where(Hero.name == "Spider-Boy")
        ).one()
        team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()

        team_z_force.heroes.append(hero_spider_boy)
        session.add(team_z_force)
        session.commit()

        print("Updated Spider-Boy's Teams:", hero_spider_boy.teams)
        print("Z-Force heroes:", team_z_force.heroes)


def update_heroes():
    with Session(engine) as session:
        hero_spider_boy = session.exec(
            select(Hero).where(Hero.name == "Spider-Boy")
        ).one()
        team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()

        hero_spider_boy.teams.remove(team_z_force)
        session.add(team_z_force)
        session.commit()

        print("Z-Force's heroes:", team_z_force.heroes)
        print("Spider-Boy's teams:", hero_spider_boy.teams)


def main():
    # create_db_and_tables()
    # create_teams_and_heroes()
    # update_teams()
    update_heroes()
    # delete_heroes()


if __name__ == "__main__":
    main()
