import sqlite3
import re
import bcrypt
salt = bcrypt.gensalt()


def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


def validate_date(date):
    pattern = "^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$"
    return re.match(pattern, date) is not None


def validate_rating(rating):
    rating = [*rating]
    print(rating)
    if len(rating) == 3:
        if int(rating[0]) > 5:
            return False
        elif rating[1] != ".":
            return False
        elif rating[2] != "0" and rating[2] != "5":
            return False
        else:
            return True
    elif len(rating) == 1:
        if int(rating[0]) > 5:
            return False
        else:
            return True
    else:
        return False


def print_rating(rating):
    rating = [*str(rating)]
    if rating[2] == "0":
        return rating[0] + " stars"
    elif rating[2] == "5":
        return rating[0] + " and a half stars"


conn = sqlite3.connect("database.db")
c = conn.cursor()

logged_in = False
while True:
    # when not logged in
    if not logged_in:
        print("\nWhat would you like to do?\n"
              "1. Create an account\n"
              "2. Login\n"
              "3. View all reviews for a movie\n"
              "4. Exit")
        x = input(">> ")
        print("")
        # create account
        if x == "1":
            f_name = input("Enter your first name:  ")
            l_name = input("Enter your last name:  ")
            date_b = input("Enter your date of birth: ")
            email_address = input("Enter an email for the account:  ")
            password = input("Create a password:  ")
            if validate_date(date_b):
                if validate_email(email_address):
                    c.execute("SELECT email FROM User_Table WHERE email = ?", (email_address,))
                    x = c.fetchall()
                    if len(x) >= 1:
                        print("A user with that email already exists. ")
                    else:
                        password = bytes(password, "UTF-8")
                        hash_password = bcrypt.hashpw(password, salt)
                        c.execute("INSERT INTO User_Table(first_name, last_name, dob, email, password) "
                                  "VALUES (?, ?, ?, ?, ?)", (f_name, l_name, date_b, email_address, hash_password))
                        conn.commit()
                        print("Account created. ")
                else:
                    print("Please enter a valid email. ")
            else:
                print("Please enter a valid date. ")
        # login
        elif x == "2":
            print("Enter your email address:  ")
            e = input(">> ")
            print("Enter your password:  ")
            p = input(">> ")
            p = bytes(p, "UTF-8")
            c.execute("SELECT password, userID FROM User_Table WHERE email = ?", (e,))
            x = c.fetchall()
            try:
                id_u = x[0][1]
                x = x[0][0]
                if bcrypt.hashpw(p, x) == x:
                    print("You have logged in. ")
                    logged_in = True
                    current_user = int(id_u)
                else:
                    print("Incorrect email or password. ")
            except:
                print("Invalid")
        # movie reviews
        elif x == "3":
            c.execute("SELECT movieID, movie_title FROM Movie_Table")
            movies = c.fetchall()
            for item in movies:
                print(str(item[0]) + ". " + item[1])
            print("Enter the number of the movie you want to view. ")
            m = input(">> ")
            print("")
            try:
                m = int(m)
                c.execute("SELECT movieID FROM Movie_Table")
                length = c.fetchall()
                if length[len(length) - 1][0] >= m > 0:
                    c.execute("SELECT movieID, movie_title FROM Movie_Table WHERE movieID = ?", (m,))
                    x = c.fetchall()
                    movie = x[0][0]
                    title = x[0][1]
                    if movie:
                        c.execute("SELECT rating FROM Review_Table WHERE movieID = ?", (movie,))
                        reviews = c.fetchall()
                        if len(reviews) > 0:
                            print("Reviews for", title + ": ")
                            for item in reviews:
                                print(print_rating(item[0]))
                        else:
                            print("No reviews")
                else:
                    print("Please enter a valid number. ")
            except:
                print("Invalid")

        elif x == "4":
            break
        else:
            print("Please enter a valid number. ")

    # when logged in
    else:
        print("\nWhat would you like to do:\n"
              "1. Logout\n"
              "2. Create a review\n"
              "3. Delete a review\n"
              "4. View all reviews for a movie\n"
              "5. Delete account\n"
              "6. Exit")
        x = input(">> ")
        print("")
        if x == "1":
            logged_in = False
            current_user = None
        # create review
        elif x == "2":
            c.execute("SELECT movieID, movie_title FROM Movie_Table")
            movies = c.fetchall()
            for item in movies:
                print(str(item[0]) + ". " + item[1])
            print("Enter the number of the movie you want to rate. ")
            m = input(">> ")
            print("")
            try:
                m = int(m)
                c.execute("SELECT movieID FROM Movie_Table")
                length = c.fetchall()
                if m <= length[len(length) - 1][0] and m > 0:
                    print("Please enter your rating as a number between 1 and 5 stars, half stars included, e.g. 4.5, 2")
                    print("Enter your rating for this movie: ")
                    x = input(">> ")
                    print("")
                    if validate_rating(x):
                        rate = float(x)
                        c.execute("INSERT INTO Review_Table (movieID, userID, rating) VALUES "
                                  "(?, ?, ?)", (m, current_user, rate))
                        conn.commit()
                        print("Your rating has been stored. ")
                    else:
                        print("Please enter a valid rating.")
                else:
                    print("Please enter a valid number. ")
            except:
                print("Invalid")

        elif x == "3":
            c.execute("SELECT reviewID, movieID, rating FROM Review_Table WHERE UserID = ?",
                      (current_user, ))
            x = c.fetchall()
            id = x[0]
            for i in range(len(id)-1):
                c.execute("SELECT movie_title FROM Movie_Table WHERE movieID = ?", (x[i][1],))
                y = c.fetchall()
                print(str(x[i][0]) + ".", y[0][0], ":", x[i][2])
            print("Pick the review you want to delete. ")
            x = input(">> ")
            try:
                c.execute("DELETE FROM Review_Table WHERE reviewID = ?", (x,))
                conn.commit()
                print("Your review has been deleted. ")
            except:
                print("Invalid")
        # movie reviews
        elif x == "4":
            c.execute("SELECT movieID, movie_title FROM Movie_Table")
            movies = c.fetchall()
            for item in movies:
                print(str(item[0]) + ". " + item[1])
            print("Enter the number of the movie you want to view. ")
            m = input(">> ")
            print("")
            try:
                m = int(m)
                c.execute("SELECT movieID FROM Movie_Table")
                length = c.fetchall()
                if m <= length[len(length) - 1][0] and m > 0:
                    c.execute("SELECT movieID, movie_title FROM Movie_Table WHERE movieID = ?", (m,))
                    x = c.fetchall()
                    movie = x[0][0]
                    title = x[0][1]
                    if movie:
                        c.execute("SELECT rating FROM Review_Table WHERE movieID = ?", (movie,))
                        reviews = c.fetchall()
                        if len(reviews) > 0:
                            print("Reviews for", title + ": ")
                            for item in reviews:
                                print(print_rating(item[0]))
                        else:
                            print("No reviews")
                else:
                    print("Please enter a valid number. ")
            except:
                print("Invalid")
        elif x == "5":
            c.execute("DELETE FROM User_Table WHERE userID = ?", (current_user, ))
            conn.commit()
            print("Your account has been deleted. ")
            logged_in = False
        elif x == "6":
            break

        else:
            print("Please enter a valid number. ")


conn.commit()
conn.close()
