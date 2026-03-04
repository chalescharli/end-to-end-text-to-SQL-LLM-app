import sqlite3

##connect to the database
conn = sqlite3.connect('student.db')

##create a cursor
c = conn.cursor()

##create a table
c.execute('''DROP TABLE IF EXISTS STUDENT''')
table_info = '''CREATE TABLE STUDENT ( NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), ROLL INTEGER)'''
c.execute(table_info)

##insert data into the table
c.execute('''INSERT INTO STUDENT VALUES ('Rishi', '10th', 'A', 1)''')
c.execute('''INSERT INTO STUDENT VALUES ('blessy', '10th', 'A', 2)''')
c.execute('''INSERT INTO STUDENT VALUES ('Rishika', '10th', 'A', 3)''')
c.execute('''INSERT INTO STUDENT VALUES ('choti', '10th', 'A', 4)''')
c.execute('''INSERT INTO STUDENT VALUES ('nihar', '12th', 'A', 5)''')
c.execute('''INSERT INTO STUDENT VALUES ('dipayan', '12th', 'A', 6)''')

# Add more sample data
import random
names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack',
         'Kate', 'Liam', 'Mia', 'Noah', 'Olivia', 'Peter', 'Quinn', 'Ryan', 'Sophia', 'Tyler',
         'Uma', 'Victor', 'Wendy', 'Xander', 'Yara', 'Zoe', 'Aaron', 'Bella', 'Caleb', 'Daisy',
         'Ethan', 'Fiona', 'Gavin', 'Hannah', 'Isaac', 'Jasmine', 'Kevin', 'Luna', 'Mason', 'Nora',
         'Owen', 'Piper', 'Quincy', 'Riley', 'Samuel', 'Tessa', 'Ulysses', 'Violet', 'Wyatt', 'Xena',
         'Yusuf', 'Zara', 'Adrian', 'Bianca', 'Cameron', 'Delilah', 'Elijah', 'Felicity', 'Gabriel', 'Harper',
         'Ian', 'Julia', 'Kai', 'Lila', 'Miles', 'Nina', 'Oscar', 'Phoebe', 'Quentin', 'Rose',
         'Sebastian', 'Talia', 'Uriah', 'Victoria', 'Xavier', 'Yasmine', 'Zachary', 'Amelia', 'Benjamin', 'Chloe',
         'Daniel', 'Emma', 'Finn', 'Gabriella', 'Hunter', 'Isabella', 'Julian', 'Katherine', 'Leo', 'Madison',
         'Nathan', 'Natalie', 'Oliver', 'Penelope', 'Quinn', 'Rebecca', 'Samuel', 'Sofia', 'Theodore', 'Valentina',
         'William', 'Abigail', 'James', 'Elizabeth', 'Michael', 'Sarah', 'David', 'Emily', 'John', 'Jessica']

classes = ['7th', '8th', '9th', '10th', '11th', '12th']
sections = ['A', 'B', 'C', 'D', 'E']

roll_start = 7
for i in range(94):  # Add 94 more to make ~100 total
    name = random.choice(names)
    class_ = random.choice(classes)
    section = random.choice(sections)
    roll = roll_start + i
    c.execute(f"INSERT INTO STUDENT VALUES ('{name}', '{class_}', '{section}', {roll})")

##execute the data insertion
print("Inserting data into the table...")
c.execute('''SELECT COUNT(*) FROM STUDENT''')
count = c.fetchone()
print(f"Total records: {count[0]}")

c.execute('''SELECT * FROM STUDENT LIMIT 10''')
data = c.fetchall()

for row in data:
    print(row)

##close the connection
conn.commit()
conn.close()