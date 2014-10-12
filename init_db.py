import sqlite3
conn = sqlite3.connect('posts.db')

c = conn.cursor()

c.execute("CREATE TABLE dilemmas (question, option1, option2, datetime, votes1, votes2, id INTEGER PRIMARY KEY)")
c.execute("INSERT INTO dilemmas VALUES ('yes or no', 'yes', 'no', 100, 20, 20, 0)")
conn.commit()
conn.close()
