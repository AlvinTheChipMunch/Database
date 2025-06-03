from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    age = Column(Integer)
    grade = Column(Integer)
    course = relationship("Student", back_populates='student')

    def __repr__(self):
        return f"Student(name={self.name}, age={self.age}, grade={self.grade}"

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'))
    student = relationship("Student", back_populates='courses')

    def __repr__(self):
        return f"Course(title={self.title}"

class Database:
    def __init__(self):
        self.engine = create_engine("sqlite:///database.db")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_student(self) -> None:
        try:
            name = input("Enter student name:")
            age = int(input("Enter student age:"))
            grade = int(input("Enter student grade:"))

            new_student = Student(name=name, age=age, grade=grade)
            self.session.add(new_student)
            self.session.commit()
            print("Student Added!")
        except Exception as e:
            print("Error:", e)
            self.session.rollback()

    def delete_student(self) -> None:
        try:
            student_id = int(input("Enter the student id: "))
            student = self.session.query(Student).filter_by(id=student_id).first()

            if student:
                self.session.delete(student)
                self.session.commit()
            else:
                print("Student not found!")
        except Exception as e:
                print(f"ERROR: {e}")
                self.session.rollback()

    def display_all_students(self) -> None:
        students = self.session.query(Student).all()
        for student in students:
            print(f"ID: {student.id}, Name: {student.name}, Age: {student.age}")
        
    def run(self) -> None:
        menu_options = {
            "1" : ("Add new student", self.add_student),
            "2" : ("Display all students", self.display_all_students),
            "3" : ("Delete student", self.delete_student),
            "7" : ("Exit", None)
        }

        while True:
            print("Database System")
            for key, (option, _) in menu_options.items():
                print(f"({key}:{option}")

            choice = input("Enter your choice (1-7):")
            if choice == "7":
                print("Goodbye")
                break

            if choice in menu_options:
                menu_options[choice][1]()
            else:
                print("Invalid Choice")

def main():
    db = Database()
    db.run()

if __name__ == "__main__":
    main()