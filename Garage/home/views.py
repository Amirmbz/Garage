from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash


db = SQL("sqlite:///garage.db")


# Create your views here.
def index(request):
    return render(request, 'home/index.html')


def register(request):
    """Register user"""
    # Forget any user_id
    request.session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Assinging username and password
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username and password was submitted
        if not username or not password:
            return HttpResponseRedirect(reverse("home:register", {
                "error": "enter username and password"
            }))

        # Ensure confirmation was submitted
        elif request.form.get("confirmation") != password:
            return HttpResponseRedirect(reverse("home:register", {
                "error": "password and confirmation didn't match"
            }))

        # Ensure username isn't already in the database
        elif len(db.execute(
            "SELECT * FROM users WHERE username = ?",
            username
        )) != 0:
            return HttpResponseRedirect(reverse("home:register", {
                "error": "username is taken"
            }))

        # Insert the username and password into database
        transaction = db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            generate_password_hash(password)
        )

        # Query database for the username that we just have created
        transaction = db.execute(
            "SELECT * FROM users WHERE username = ?",
            username
        )

        # Remember which user has logged in
        request.session["user_id"] = transaction[0]["id"]

        # Redirect user to home page
        return HttpResponseRedirect("home:index")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render(request, 'home/register.html')


def login(request):
    """Log user in"""

    # Forget any user_id
    request.session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Assinging username and password
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username and password was submitted
        if not username or not password:
            return HttpResponseRedirect(reverse("home:login", {
                "error": "enter username and password"
            }))

        # Query database for username
        transaction = db.execute(
            "SELECT * FROM users WHERE username = ?",
            username
        )

        # Ensure username exists and password is correct
        if len(transaction) != 1 or not check_password_hash(
            transaction[0]["hash"], password
        ):
            return HttpResponseRedirect(reverse("home:login", {
                "error": "invalid username and/or password"
            }))

        # Remember which user has logged in
        request.session["user_id"] = transaction[0]["id"]

        # Redirect user to home page
        return HttpResponseRedirect("home:index")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render(request, 'home/login.html')


def logout(request):
    """Log user out"""

    # Forget any user_id
    request.session.clear()

    # Redirect user to login form
    return HttpResponseRedirect("home:index")
