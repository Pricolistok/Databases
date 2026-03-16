import datetime
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, Date, Time, ForeignKey, func, text, extract
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = f"postgresql://prico:1234@localhost:5433/rk3"

engine = create_engine(DATABASE_URL)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Driver(Base):
    __tablename__ = 'driver'
    id = Column(Integer, primary_key=True)
    fio = Column(String)
    birth_date = Column(Date)
    hire_date = Column(Date)
    region = Column(String)
    routes = relationship("Route", back_populates="driver")

class Route(Base):
    __tablename__ = 'route'
    id = Column(Integer, primary_key=True)
    driver_id = Column(Integer, ForeignKey('driver.id'))
    route_date = Column(Date)
    route_time = Column(Time)
    day_of_week = Column(String)
    arrival_type = Column(Integer)
    driver = relationship("Driver", back_populates="routes")

print("ЗАПРОС 1: Регионы, в которых работает более 15 водителей")

sql1 = text("""
    SELECT region 
    FROM driver 
    GROUP BY region 
    HAVING COUNT(id) > 15
""")

res1_sql = session.execute(sql1).fetchall()
print(f"SQL результат: {res1_sql}")

res1_orm = session.query(Driver.region).\
    group_by(Driver.region).\
    having(func.count(Driver.id) > 15).all()
print(f"ORM результат: {res1_orm}\n")


print("ЗАПРОС 2: Водители, которые в прошлом году вернулись последними")
sql2 = text("""
    SELECT * FROM driver 
    WHERE id IN (
        SELECT driver_id FROM route 
        WHERE arrival_type = 0 
        AND EXTRACT(YEAR FROM route_date) = 2024
        AND (route_date + route_time) = (
            SELECT MAX(route_date + route_time) 
            FROM route 
            WHERE arrival_type = 0 
            AND EXTRACT(YEAR FROM route_date) = 2024
        )
    )
""")
res2_sql = session.execute(sql2).fetchall()
print(f"SQL результат: {[r.fio for r in res2_sql]}")

max_time_subq = session.query(func.max(Route.route_date + Route.route_time)).\
    filter(Route.arrival_type == 0, extract('year', Route.route_date) == 2024).scalar_subquery()

res2_orm = session.query(Driver).\
    join(Route).\
    filter(
        Route.arrival_type == 0,
        extract('year', Route.route_date) == 2024,
        (Route.route_date + Route.route_time) == max_time_subq
    ).all()
print(f"ORM результат: {[d.fio for d in res2_orm]}\n")


print("ЗАПРОС 3: Московские водители, чей последний рейс в 2025 году был не позднее 17 октября")

sql3 = text("""
    SELECT * FROM driver 
    WHERE region = 'Москва' 
    AND id IN (
        SELECT driver_id 
        FROM route 
        WHERE EXTRACT(YEAR FROM route_date) = 2025
        GROUP BY driver_id
        HAVING MAX(route_date) <= '2025-10-17'
    )
""")
res3_sql = session.execute(sql3).fetchall()
print(f"SQL результат: {[r.fio for r in res3_sql]}")

drivers_subq = session.query(Route.driver_id).\
    filter(extract('year', Route.route_date) == 2025).\
    group_by(Route.driver_id).\
    having(func.max(Route.route_date) <= datetime.date(2025, 10, 17)).scalar_subquery()

res3_orm = session.query(Driver).\
    filter(Driver.region == 'Москва', Driver.id.in_(drivers_subq)).all()
print(f"ORM результат: {[d.fio for d in res3_orm]}")

session.close()
