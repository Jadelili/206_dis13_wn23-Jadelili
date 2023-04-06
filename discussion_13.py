import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


# TASK 1
# CREATE TABLE FOR EMPLOYEE INFORMATION IN DATABASE AND ADD INFORMATION
def create_employee_table(cur, conn):
    cur.execute('''CREATE TABLE IF NOT EXISTS employees ("employee_id" INTEGER PRIMARY KEY, 
    "first_name" TEXT, "last_name" TEXT, "job_id" INTEGER, "hire_date" TEXT, "salary" NUMERIC)''')


# ADD EMPLOYEE'S INFORMTION TO THE TABLE
def add_employee(filename, cur, conn):
    #load .json file and read job data
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)))
    file_data = f.read()    # long string
    filevar = json.loads(file_data)

    for i in filevar:
        id = int(i["employee_id"])
        f_name = i["first_name"]
        l_name = i["last_name"]
        job = int(i["job_id"])
        date = i["hire_date"]
        sal = int(i["salary"])
        cur.execute('''INSERT OR IGNORE INTO employees (employee_id, first_name, last_name, job_id, 
                hire_date, salary) VALUES (?,?,?,?,?,?)''', (id, f_name, l_name, job, date, sal))
    f.close()
    conn.commit()


# TASK 2: GET JOB AND HIRE_DATE INFORMATION
def job_and_hire_date(cur, conn):
    people_list = []
    cur.execute('SELECT Employees.hire_date, Jobs.job_title FROM Employees JOIN Jobs \
                ON Employees.job_id = Jobs.job_id')
    for row in cur:
        people_list.append(row)
    yoe = sorted(people_list, key = lambda x:x[0])
    return yoe[0][1]


# TASK 3: IDENTIFY PROBLEMATIC SALARY DATA
# Apply JOIN clause to match individual employees
def problematic_salary(cur, conn):
    name_list = []
    cur.execute('SELECT Employees.first_name, Employees.last_name FROM Employees JOIN\
                Jobs ON Jobs.job_id = Employees.job_id WHERE Employees.salary < Jobs.min_salary OR\
                Employees.salary > Jobs.max_salary')
    for row in cur:
        name_list.append(row)
    return name_list


# TASK 4: VISUALIZATION
def visualization_salary_data(cur, conn):
    title_sal_list = []
    d = {}
    cur.execute('SELECT Jobs.job_title, Employees.salary FROM Employees JOIN\
                Jobs ON Jobs.job_id = Employees.job_id')
    for row in cur:
        title_sal_list.append(row)
    for tup in title_sal_list:
        d[tup[0]] = d.get(tup[0], []) + [tup[1]]  # if not exist, return an empty list
    
    # sal_list = 
    # cur.execute('SELECT Jobs.job_title, Jobs.min_salary, Jobs.max_salary \
    #         FROM Employees JOIN Jobs ON Jobs.job_id = Employees.job_id')
    # for row in cur:
    #     title_sal_list.append(row)
    
    plt.figure()
    # title_list = []
    # sa
    for title in d:
        for sal in d[title]:
            plt.scatter(title, sal)
            # plt.scatter(title, min_salary, color='red', marker='x')
    
    
    
    plt.suptitle("Title-Salary")
    plt.show()

class TestDiscussion12(unittest.TestCase):
    def setUp(self) -> None:
        self.cur, self.conn = setUpDatabase('HR.db')

    def test_create_employee_table(self):
        self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='employees'")
        table_check = self.cur.fetchall()[0][0]
        self.assertEqual(table_check, 1, "Error: 'employees' table was not found")
        self.cur.execute("SELECT * FROM employees")
        count = len(self.cur.fetchall())
        self.assertEqual(count, 13)

    def test_job_and_hire_date(self):
        self.assertEqual('President', job_and_hire_date(self.cur, self.conn))

    def test_problematic_salary(self):
        sal_list = problematic_salary(self.cur, self.conn)
        self.assertIsInstance(sal_list, list)
        self.assertEqual(sal_list[0], ('Valli', 'Pataballa'))
        self.assertEqual(len(sal_list), 4)


def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('HR.db')
    create_employee_table(cur, conn)
    add_employee("employee.json",cur, conn)
    job_and_hire_date(cur, conn)
    wrong_salary = (problematic_salary(cur, conn))
    # print(wrong_salary)
    visualization_salary_data(cur, conn)

if __name__ == "__main__":
    main()
    # unittest.main(verbosity=2)

