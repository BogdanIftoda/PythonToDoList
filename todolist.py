from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

stop = True

today = datetime.today()

while stop:
    choice = int(input('\
1) Today\'s tasks\n\
2) Week\'s tasks\n\
3) All tasks\n\
4) Missed tasks\n\
5) Add task\n\
6) Delete task\n\
0) Exit\n'))

    if choice == 1:
        task_n = 0
        rows = session.query(Task).order_by(Task.deadline).filter(Task.deadline == datetime.today().date())
        if rows.all() == []:
            print(f'\nToday {datetime.today().day} {datetime.today().strftime("%b")}:')
            print('Nothing to do!')
        else:
            for entry in rows:
                task_n += 1
                print(f'\nToday {datetime.today().day} {datetime.today().strftime("%b")}:')
                print(f'{task_n}. {entry.task}')
    elif choice == 2:
        rows = session.query(Task).order_by(Task.deadline).filter(Task.deadline <= datetime.today() + timedelta(days=7))
        row_dict = {row: row.deadline for row in rows}
        week = [datetime.today().date() + timedelta(days = i) for i in range(7)]
        for myday in week:
            task_n = 0
            if myday in row_dict.values():
                print(f'\n{myday.strftime("%A")} {myday.day} {myday.strftime("%b")}:')
                for entry in rows:
                    if entry.deadline == myday:
                        task_n += 1
                        print(f'{task_n}. {entry.task}')
            else:
                print(f'\n{myday.strftime("%A")} {myday.day} {myday.strftime("%b")}:')
                print('Nothing to do!')
    elif choice == 3:
        task_n = 0
        rows = session.query(Task).order_by(Task.deadline).all()
        if rows == []:
            print('Nothing to do!')
        else:
            print('\nAll tasks:')
            for entry in rows:
                task_n += 1
                print(f'{task_n}. {entry.task}. {entry.deadline.day} {entry.deadline.strftime("%b")}')
    elif choice == 4:
        task_n = 0
        rows = session.query(Task).filter(Task.deadline < datetime.today().date()).all()
        for entry in rows:
            task_n += 1
            print(f'{task_n}. {entry.task}. {entry.deadline.day} {entry.deadline.strftime("%b")}')
        print()

    elif choice == 5:
        new_task = input('\nEnter task\n')
        new_deadline = input('Enter deadline\n')
        if new_deadline == '':
            new_deadline = datetime.today()
        else:
            new_deadline = datetime.strptime(new_deadline, '%Y-%m-%d')
        new_row = Task(task=new_task, deadline=new_deadline)
        session.add(new_row)
        session.commit()
        print('The task has been added!')
    elif choice == 6:
        rows = session.query(Task).order_by(Task.deadline).all()

        print('Choose the number of the task you want to delete:')
        if rows == []:
            print('Nothing to delete!')
        task_n = 0
        for entry in rows:
            task_n += 1
            print(f'{task_n}. {entry.task}. {entry.deadline.day} {entry.deadline.strftime("%b")}')
        del_number = int(input())
        specific_row = rows[del_number-1]
        session.delete(specific_row)
        session.commit()
        print('The task has been deleted!')
    elif choice == 0:
        print('\nBye!')
        stop = False
