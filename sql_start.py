import sqlite3
import bcrypt
conn = sqlite3.connect("database.db")
c = conn.cursor()

create_table_statement = """CREATE TABLE IF NOT EXISTS Movie_Table (
  movieID INTEGER PRIMARY KEY,
  movie_title VARCHAR(30),
  movie_release_date VARCHAR(10),
  movie_genre VARCHAR(20)
);"""
c.execute(create_table_statement)

create_table_statement = """CREATE TABLE IF NOT EXISTS User_Table (
  userID INTEGER PRIMARY KEY,
  first_name VARCHAR(30),
  last_name VARCHAR(30),
  dob DATE,
  email VARCHAR(30),
  password VARCHAR(20)
);"""
c.execute(create_table_statement)

create_table_statement = """CREATE TABLE IF NOT EXISTS Review_Table (
  reviewID INTEGER PRIMARY KEY,
  movieID INTEGER, 
  userID INTEGER,
  rating REAL,
  FOREIGN KEY (movieID) REFERENCES Movies_Table(movieID),
  FOREIGN KEY (userID) REFERENCES Users_Table(userID)
);"""
c.execute(create_table_statement)

insert_statement = """INSERT INTO Movie_Table (movie_title, movie_release_date, movie_genre) 
VALUES ("Blue Beetle", "18/8/2023", "Science Fiction")"""
c.execute(insert_statement)

insert_statement = """INSERT INTO Movie_Table (movie_title, movie_release_date, movie_genre) 
VALUES ("Batman", "4/4/2022", "Science Fiction")"""
c.execute(insert_statement)

insert_statement = """INSERT INTO Movie_Table (movie_title, movie_release_date, movie_genre) 
VALUES ("Titanic", "19/12/1997", "Romance")"""
c.execute(insert_statement)

insert_statement = """INSERT INTO Movie_Table (movie_title, movie_release_date, movie_genre) 
VALUES ("Exorcist", "26/12/1973", "Horror")"""
c.execute(insert_statement)

insert_statement = """INSERT INTO Movie_Table (movie_title, movie_release_date, movie_genre) 
VALUES ("Brokeback Mountain", "6/1/2006", "Romance")"""
c.execute(insert_statement)

password = bytes("root", "UTF-8")
password = bcrypt.hashpw(password, bcrypt.gensalt())
c.execute("INSERT INTO User_Table (first_name, last_name, dob, email, password) VALUES (?, ?, ?, ?, ?)",
          ("Admin", "Root", "01/01/2000", "admin@gmail.com", password))

conn.commit()
conn.close()
