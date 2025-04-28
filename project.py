import sqlite3
import getpass
import sys
import time
import tabulate
import os
from datetime import datetime


conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
session_id = 102
session_name = ''

def main():
    global session_id 
    global session_name
    while True:
        selection = int(input("1. Login \n2. Signup\nEnter choice [1 or 2] : "))
        if selection == 1: 
            login = Login()
            if login == "Success":
                print("Redirecting to Task Page")
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"\nWelcome {session_name}!\n")
                display_dashboard()
                while True:
                    
                    print("\n")
                    print("1. Add a Task")
                    print("2. View Task list")
                    print("3. Mark Task as done")
                    print("4. View Completed Tasks")
                    print("5. Logout")
                    try:
                        sel2 = int(input("Enter your choice: "))
                        os.system('cls' if os.name == 'nt' else 'clear')

                        if sel2 == 1:
                            add_task()
                        elif sel2 == 2:
                            result = show_tasks()
                            if not result:
                                print("No pending tasks.")
                            else:
                                print(tabulate.tabulate(result,headers=["Project_ID","Task Name", "Priority", "Time Created", "Deadline",'Status'],tablefmt="fancy_grid",colalign=("center", "center", "center", "center", "center", "center")))
                        elif sel2 == 3:
                            mark_done()
                        elif sel2 == 4:
                            result = view_completed()
                            if not result:
                                print("No completed tasks.")
                            else:
                                print(tabulate.tabulate(result,headers=["Project_ID","Task Name", "Priority", "Time Created", "Deadline",'Status'],tablefmt="fancy_grid",colalign=("center", "center", "center", "center", "center", "center")))
                        elif sel2 == 5:
                            print("Logging out...")
                            time.sleep(1)
                            os.system('cls' if os.name == 'nt' else 'clear')
                            break
                        else:
                            print("Invalid option. Please select between 1 to 5.")
                    except ValueError:
                        print("Please enter a valid number.")
            else:
                print(login)
            break
        elif selection == 2:
            signup()
            print("\nRestart the program and login")
            time.sleep(2)
            break
        else:
            print("Wrong input\n\n")
    
    time.sleep(5)

    
        

def Login():
    global session_id
    global session_name
    username = input("Enter userID : ")
    cursor.execute("SELECT * from users where id = ?",(username,))
    res = cursor.fetchall() 
    if res:
        db_password = res[0][2]  
        i = 0
        while i < 3:
            password = getpass.getpass("Enter your password: ")
            if password == db_password:
                session_id = res[0][0]
                session_name = res[0][1]
                return("Success")
                
                
            else:
                i += 1
                print("Password Incorrect. Try again.")

        return("Incorrect password entered 3 times. Try again later.")
    else:
        return("Not found.")
 

def signup():
        print("Creating a new user...")
        name = input("Enter name : ")
        password = getpass.getpass("Enter your password: ")
        cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, password))
        conn.commit() 
        print("User added succssfully\n")



def add_task():
    task_name = input("Enter Task Name: ")
    while True:
        user_input = input("Enter deadline (YYYY-MM-DD): ")
        try:
            task_deadline = datetime.strptime(user_input, "%Y-%m-%d")
            if task_deadline <= datetime.now():
                print("Deadline must be in the future. Try again.")
            else:
                break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    task_priority = int(input("Enter Task Priority [0-9] : "))
    global session_id
    x = datetime.now()
    cursor.execute("Insert into tasks (user_id, task, priority, deadline,created) values (?,?,?,?,?)",(session_id,task_name,task_priority,task_deadline.strftime("%c"),x.strftime("%c")))
    conn.commit()

def show_tasks():
    global session_id
    global session_name
    cursor.execute("Select id, task,priority, created,deadline,status from tasks where user_id = ? and Status = ? ORder by priority",(session_id,0))
    res = cursor.fetchall()
    return res
   


def mark_done():
    result = show_tasks()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(tabulate.tabulate(result,headers=["Project_ID","Task Name", "Priority", "Time Created", "Deadline",'Status'],tablefmt="fancy_grid",colalign=("center", "center", "center", "center", "center", "center")))
    print("\n\n\n")
    task_ids = [row[0] for row in result]  
    if not task_ids:
        print("No tasks to mark as complete.")
        return
    
    while True:
        try:
            sel = int(input("Enter Task ID you want to mark as complete: "))
            if sel in task_ids:
                cursor.execute("UPDATE tasks SET status = 1 WHERE id = ? AND user_id = ?", (sel, session_id))
                conn.commit()
                print(f"Task {sel} marked as complete.")
                break
            else:
                print("Invalid Task ID. Try again.")
        except ValueError:
            print("Please enter a valid number.")



def view_completed():
    global session_id
    global session_name
    cursor.execute("Select id, task,priority, created,deadline,status from tasks where user_id = ? and Status = ? ORder by priority",(session_id,1))
    res = cursor.fetchall()
    return res

def display_dashboard():
    print("========Dashboard=======")
    # Fetch total number of tasks
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?", (session_id,))
    total = cursor.fetchall()
    
    # Ensure there's at least one result to avoid IndexError
    if total:
        total = total[0][0]  # Extract the count of total tasks

        # Fetch count of completed tasks
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND status = 1", (session_id,))
        completed = cursor.fetchall()[0][0]

        # Fetch count of pending tasks
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND status = 0", (session_id,))
        pending = cursor.fetchall()[0][0]

        # Fetch count of overdue tasks
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND status = 0 AND deadline < ?", (session_id, datetime.now().strftime("%c")))
        overdue = cursor.fetchall()[0][0]

        # Print the dashboard
        print(f"Total Tasks    : {total}")
        print(f"Completed      : {completed}")
        print(f"Pending        : {pending}")
        print(f"Overdue        : {overdue}")
        print("\n=============================\n")
    else:
        print("No tasks found.")

if __name__ == '__main__':
    main()
