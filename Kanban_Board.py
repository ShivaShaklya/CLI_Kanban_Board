import mysql.connector as con

def create_new_board():
    name=input("Enter new board name: ")
    try:
        cur.execute("""
        CREATE TABLE {}(
            task_id INT AUTO_INCREMENT PRIMARY KEY,
            task_name VARCHAR(255) NOT NULL,
            status int NOT NULL
        );
        """.format(name))
    except:
        print("Board already exists")

def display_board(board):
    ToDo=[]
    InPro=[]
    Done=[]
    cur.execute("select task_name, status from {}".format(board))
    tasks=cur.fetchall()
    for i in tasks:
        if(i[1]==0):
            ToDo.append(i[0])
        elif(i[1]==1):
            InPro.append(i[0])
        elif(i[1]==2):
            Done.append(i[0])
    
    print()
    print("TO DO")
    for i in range (len(ToDo)):
        print(str(i+1)+". ",ToDo[i])
    print()
    print("IN PROGRESS")
    for i in range (len(InPro)):
        print(str(i+1)+". ",InPro[i])
    print()
    print("DONE")
    for i in range (len(Done)):
        print(str(i+1)+". ",Done[i])
    print()

    return ToDo,InPro,Done

def Add_Task(board):
    task_name=input("Enter task name: ")
    status=int(input("Enter Status(0: To Do, 1: In progress, 2: Done): "))
    values=(task_name,status)
    q="insert into {}(task_name, status) values (%s, %s)".format(board)
    cur.execute(q,values)
    mycon.commit()
    print("task added")

def Delete_Task(board):
    all_status = {0:ToDo, 1:InPro, 2:Done}
    status = int(input("Enter Status (0: To Do, 1: In progress, 2: Done): "))
    task_no = int(input("Enter task no.: "))
    status_list=all_status.get(status)
    try:
        if status_list is not None:
            q="delete from {} where task_name=%s".format(board)
            cur.execute(q,(status_list[task_no-1],))
            mycon.commit()
            print("Task deleted successfully.")
        else:
            print("Invalid status.")
    except Exception as e:
        print("An error occurred:", e)

##
p=input("Enter your mysql password: ")
mycon=con.connect(host="localhost", user="root", password=p)
cur=mycon.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS kanban")
cur.execute("USE kanban")
try: 
    cur.execute("""
        CREATE TABLE IF NOT EXISTS kanban_board (
            task_id INT AUTO_INCREMENT PRIMARY KEY,
            task_name VARCHAR(255) NOT NULL,
            status int NOT NULL
        );
    """)
except con.Error as err:
    print("Failed creating table: {}".format(err))
##
print("KANBAN BOARDS")
cur.execute("show tables;")
boards=cur.fetchall()
ctr=0
n=len(boards)

for i in boards:
    print(str(ctr)+". ",i[0])
    ctr+=1
print(str(ctr)+". ","Create New Board")

choice=int(input("Enter Board no.: "))
if(choice==ctr):
    create_new_board()
else:
    board=boards[choice-1][0]
    ToDo,InPro,Done=display_board(board)

c=0
while(c!=4):
    print("1. Add new Task\n2. Delete a task\n3. Display Board\n4. Exit")
    c=int(input("Enter choice: "))
    if (c==1):
        Add_Task(board)
    elif(c==2):
        Delete_Task(board)
    elif (c==3):
        ToDo,InPro,Done=display_board(board)

