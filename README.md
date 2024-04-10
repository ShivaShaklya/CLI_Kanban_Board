CLI Kanban Board

A kanban board is used to track the status and priorities of various subtasks to be done in a software project. 

A simple code using command line to organize different tasks across different projects. Uses mysql to maintain individual kanaban boards as seperate tables.
Each table comprises of the task_id(sno.), task_name, status (0: To do, 1: In Progress, 2: Done), priority (0: Low, 1:Medium, 2: High), Assignee_id  and reporter_id.
The python script manipulates and displays the data stored in the mysql database in a coherent and user - friendly manner.
