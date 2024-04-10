import mysql.connector as con

def create_new_board():
    name=input("Enter new board name: ")
    try:
        cur.execute("""
        CREATE TABLE {}(
            task_id INT AUTO_INCREMENT PRIMARY KEY,
            task_name VARCHAR(255) NOT NULL,
            status int NOT NULL,
            priority int NOT NULL,
            assignee_id varchar(10) NOT NULL,
            reporter_id varchar(10) NOT NULL 
        );
        """.format(name))
    except:
        print("Board already exists")

def display_board(board):
    ToDo=[]
    InPro=[]
    Done=[]
    p1=[]
    p2=[]
    p3=[]
    priority={0:"Low",1:"Medium",2:"High"}
    cur.execute("select task_name, status, priority from {}".format(board))
    tasks=cur.fetchall()
    for i in tasks:
        if(i[1]==0):
            ToDo.append(i[0])
            p1.append(priority.get(i[2]))
        elif(i[1]==1):
            InPro.append(i[0])
            p2.append(priority.get(i[2]))
        elif(i[1]==2):
            Done.append(i[0])
            p3.append(priority.get(i[2]))
    
    print()
    print("TO DO")
    for i in range (len(ToDo)):
        print(str(i+1)+". ",ToDo[i],"    ",p1[i])
    print()
    print("IN PROGRESS")
    for i in range (len(InPro)):
        print(str(i+1)+". ",InPro[i],"    ",p2[i])
    print()
    print("DONE")
    for i in range (len(Done)):
        print(str(i+1)+". ",Done[i],"    ",p3[i])
    print()

    return ToDo,InPro,Done,p1,p2,p3

def Add_Task(board):
    task_name=input("Enter task name: ")
    status=int(input("Enter Status(0: To Do, 1: In progress, 2: Done): "))
    priority=int(input("Enter priority(0: Low, 1: Medium, 2: High): "))
    assignee_id=input("Enter assignee_id: ")
    reporter_id=input("Enter reporter id: ")
    values=(task_name,status,priority,assignee_id,reporter_id)
    q="insert into {}(task_name, status,priority,assignee_id,reporter_id) values (%s, %s,%s,%s,%s)".format(board)
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

def Sort(board):
    status_list=[ToDo,InPro,Done]
    priority_list=[p1,p2,p3]

    for k in priority_list:
        for m in range(len(k)):
            if(k[m]=="High"):
                k[m]=2
            elif(k[m]=="Medium"):
                k[m]=1
            elif(k[m]=="Low"):
                k[m]=0
    
    print(status_list[0],p1)
    for l in range (len(priority_list)):
        p_list=priority_list[l]
        s_list=status_list[l]
        for i in range(len(p_list)):
            for j in range(len(p_list)):
                if(p_list[i]>p_list[j]):
                    p_list[i],p_list[j]=p_list[j],p_list[i]
                    s_list[i],s_list[j]=s_list[j],s_list[i]

    print(ToDo,p1)
    priority={0:"Low",1:"Medium",2:"High"}
    
    print()
    print("TO DO")
    for i in range (len(ToDo)):
        print(str(i+1)+". ",ToDo[i],"    ",priority.get(p1[i]))
    print()
    print("IN PROGRESS")
    for i in range (len(InPro)):
        print(str(i+1)+". ",InPro[i],"    ",priority.get(p2[i]))
    print()
    print("DONE")
    for i in range (len(Done)):
        print(str(i+1)+". ",Done[i],"    ",priority.get(p3[i]))
    print()

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
            status int NOT NULL,
            priority int NOT NULL,
            assignee_id varchar(10) NOT NULL,
            reporter_id varchar(10) NOT NULL 
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
    ToDo,InPro,Done,p1,p2,p3=display_board(board)

c=0
while(c!=5):
    print("1. Add new Task\n2. Delete a task\n3. Sort Tasks\n4. Display Board\n5. Exit")
    c=int(input("Enter choice: "))
    if (c==1):
        Add_Task(board)
    elif(c==2):
        Delete_Task(board)
    elif(c==3):
        Sort(board)
    elif (c==4):
        ToDo,InPro,Done,p1,p2,p3=display_board(board)

