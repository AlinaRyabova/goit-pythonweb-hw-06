from sqlite3 import Error

from connect import create_connection, database

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e)

if __name__ == '__main__':
    sql_create_projects_table = """
    CREATE TABLE IF NOT EXISTS projects (
     id integer PRIMARY KEY,
     name text NOT NULL,
     begin_date text,
     end_date text
    );
    """

    sql_create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
     id integer PRIMARY KEY,
     name text NOT NULL,
     priority integer,
     project_id integer NOT NULL,
     status Boolean default False,
     begin_date text NOT NULL,
     end_date text NOT NULL,
     FOREIGN KEY (project_id) REFERENCES projects (id)
    );
    """


    with create_connection(database) as conn:
        if conn is not None:
            # create projects table
            create_table(conn, sql_create_projects_table)
            # create tasks table
            create_table(conn, sql_create_tasks_table)
        else:
            print("Error! cannot create the database connection.")

def create_project(conn, project):
    sql = '''
    INSERT INTO projects(name,begin_date,end_date) VALUES(?,?,?);
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, project)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

    return cur.lastrowid

def create_task(conn, task):
    sql = '''
    INSERT INTO tasks(name,priority,status,project_id,begin_date,end_date) VALUES(?,?,?,?,?,?);
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, task)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

    return cur.lastrowid 

if __name__ == '__main__':
    with create_connection(database) as conn:
        # create a new project
        project = ('Cool App with SQLite & Python', '2022-01-01', '2022-01-30')
        project_id = create_project(conn, project)
        print(project_id)

        # tasks
        task_1 = ('Analyze the requirements of the app', 1, True, project_id, '2022-01-01', '2022-01-02')
        task_2 = ('Confirm with user about the top requirements', 1, False, project_id, '2022-01-03', '2022-01-05')

        # create tasks
        print(create_task(conn, task_1))
        print(create_task(conn, task_2))