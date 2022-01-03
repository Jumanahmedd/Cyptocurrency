# Cyptocurrency

In order for this code to run, an interpreter is needed to run the python code and some commands should be run in the terminal to be able to create and access the database. MYSQL should also be installed for these commands to work from this URL(https://dev.mysql.com/downloads/installer/). The commands should be run in the command prompt in the order below: 
1.	Pip install flask
2.	Pip install flask-mysqldb
3.	Pip install passlib
4.	Enter cd\ then type “net start”
5.	Then type “dir mysqld.exe /s /p”, then something like "Directory of C:\Program Files\MySQL\MySQL Server 8.0\bin" will be outputted in the terminal
6.	Type cd then copy and paste the directory that was outputted above
7.	Type and run “mysql –uroot –p”, then enter the MySQL password
8.	CREATE DATABASE crypto;
9.	USE crypto;
10.	CREATE TABLE blockchain( number varchar(10), hash varchar(64), previous varchar(64), data varchar(100), nonce varchar(15));
11.	SELECT * from blockchain;
12.	CREATE TABLE users(name varchar(30), username varchar(30), email varchar(50), password varchar(100));
13.	Pip install wtforms
14.	Pip install functools
After running theses commands, the app.py file is run either in an interpreter like visual code or in a terminal by simply typing python and the name of the file or file destination. After the file is run the output should be similar to the output in figure . To display the website on the browser you can either copy and paste the URL outputted by the terminal which is http://127.0.0.1:5000/, or go to the browser and type localhost:5000. 5000 because the port number the file is running on.  

This program is created using python version 3.9.9, html 5, css, JavaScript and MySQL. The steps to run the code is explained in details above. 
