from sqlalchemy.orm import aliased, sessionmaker
from sqlalchemy import func
from models import Student, Group, Teacher, Subject, Grade, init_db
from colorama import Fore, Style, init

# Ініціалізація сесії
engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()

# Ініціалізація colorama
init(autoreset=True)

# Округлення результатів
def round_results(results):
    if isinstance(results, tuple):
        return tuple(
            round(value, 2) if isinstance(value, float) else value for value in results
        )
    elif isinstance(results, list):
        return [round_results(result) for result in results]
    return results

# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів
def select_1():
    result = (
        session.query(Student.name, func.avg(Grade.grade).label("average_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )
    return round_results(result)

# 2. Знайти студента із найвищим середнім балом з певного предмета
def select_2(subject_name):
    result = (
        session.query(Student.name, func.avg(Grade.grade).label("average_grade"))
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )
    if result:
        return round_results([result])[0]
    return result

# 3. Знайти середній бал у групах з певного предмета
def select_3(subject_name):
    SubjectAlias = aliased(Subject)

    query = (
        session.query(Group.name, func.avg(Grade.grade).label("average_grade"))
        .select_from(Group)
        .join(Student)
        .join(Grade, Grade.student_id == Student.id)
        .join(SubjectAlias, SubjectAlias.id == Grade.subject_id)
        .filter(SubjectAlias.name == subject_name)
        .group_by(Group.name)
        .all()
    )

    return round_results(query)

# 4. Знайти середній бал на потоці (по всій таблиці оцінок)
def select_4():
    result = session.query(func.avg(Grade.grade).label("average_grade")).scalar()
    if result is not None:
        return round(result, 2)
    return result

# 5. Знайти які курси читає певний викладач
def select_5(teacher_name):
    result = (
        session.query(Subject.name)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    return result

# 6. Знайти список студентів у певній групі
def select_6(group_name):
    result = (
        session.query(Student.name).join(Group).filter(Group.name == group_name).all()
    )
    return result

# 7. Знайти оцінки студентів у окремій групі з певного предмета
def select_7(group_name, subject_name):
    result = (
        session.query(Student.name, Grade.grade)
        .join(Group)
        .join(Grade)
        .join(Subject)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )
    return result

# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів
def select_8(teacher_name):
    result = (
        session.query(func.avg(Grade.grade).label("average_grade"))
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .scalar()
    )
    return round(result, 2) if result is not None else result

# 9. Знайти список курсів, які відвідує певний студент
def select_9(student_name):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .filter(Student.name == student_name)
        .all()
    )
    return result

# 10. Список курсів, які певному студенту читає певний викладач
def select_10(student_name, teacher_name):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .join(Teacher)
        .filter(Student.name == student_name, Teacher.name == teacher_name)
        .all()
    )
    return result

# Функція для виведення результатів
def print_query_result(query_result, title):
    print(Fore.CYAN + Style.BRIGHT + title)
    if query_result:
        for row in query_result:
            print(Fore.GREEN + str(row))
    else:
        print(Fore.RED + "Результатів не знайдено.")
    print("\n" + "-" * 50)

if __name__ == "__main__":
    # Приклад використання функцій з кольоровим виведенням та округленням
    print_query_result(select_1(), "Топ 5 студентів за середнім балом")

    student_2 = select_2("Financial")
    if student_2:
        print_query_result([student_2], "Студент з найвищим середнім балом з  Financial")
    else:
        print(Fore.RED + "Студента з найвищим середнім балом з  Financial не знайдено.")

    select_3_result = select_3("Drive")
    if select_3_result:
        print_query_result(select_3_result, "Середній бал у групах з предмета 'Drive'")
    else:
        print(Fore.RED + "Групи для предмета 'Drive' не знайдено.")

    overall_avg = select_4()
    if overall_avg is not None:
        print(Fore.YELLOW + f"Загальний середній бал: {overall_avg}")
    else:
        print(Fore.RED + "Не знайдено середнього балу.")

    select_5_result = select_5("Joseph Lopez")
    if select_5_result:
        print_query_result(select_5_result, "Курси, які читає Joseph Lopez")
    else:
        print(Fore.RED + "Не знайдено курсів, які викладає Joseph Lopez.")

    select_6_result = select_6("Група 1")
    if select_6_result:
        print_query_result(select_6_result, "Студенти у групі 1")
    else:
        print(Fore.RED + "Не знайдено студентів у групі 1.")

    select_7_result = select_7("Група 1", "Drive")
    if select_7_result:
        print_query_result(select_7_result, "Оцінки студентів у групі 1 з предмета 'Drive'")
    else:
        print(Fore.RED + "Не знайдено оцінок у групі 1 з предмета 'Drive'.")

    avg_8 = select_8("Joseph Lopez")
    if avg_8 is not None:
        print(Fore.YELLOW + f"Середній бал Joseph Lopez: {avg_8}")
    else:
        print(Fore.RED + "Не знайдено середнього балу для Joseph Lopez.")

    select_9_result = select_9("Angela Foster")
    if select_9_result:
        print_query_result(select_9_result, "Курси, які відвідує Angela Foster")
    else:
        print(Fore.RED + "Не знайдено курсів для Angela Foster.")

    select_10_result = select_10("Angela Foster", "Joseph Lopez")
    if select_10_result:
        print_query_result(
            select_10_result, "Курси, які Joseph Lopez читає для Angela Foster"
        )
    else:
        print(Fore.RED + "Не знайдено курсів для Angela Foster, які викладає Joseph Lopez.")
