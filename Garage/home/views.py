from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password


# Create your views here.
def index(request):
    return render(request, 'home/index.html')


def register(request):
    """Register user"""
    # Forget any user_id
    logout(request)
    request.session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Assinging username and password
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Ensure username and password was submitted
        if not username or not password:
            return render(request, "home/register.html", {
                "error": "enter username and password"
            })

        # Ensure confirmation was submitted
        elif request.POST.get("confirmation") != password:
            return render(request, "home/register.html", {
                "error": "password and confirmation didn't match"
            })

        # Ensure username isn't already in the database
        if User.objects.filter(username=username).exists():
            return render(request, "home/register.html", {
                "error": "Username is already taken."
            })

        # Insert the username and password into database
        user = User.objects.create(
            username=username,
            password=make_password(password)
            )
        user.save()

        # Log the user in
        login(request, user)

        # Redirect user to home page render(request, 'home/index.html')
        return redirect('index')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render(request, 'home/register.html')


def log_in(request):
    """Log user in"""

    # Forget any user_id
    logout(request)
    request.session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Assinging username and password
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Ensure username and password was submitted
        if not username or not password:
            return render(request, 'home/login.html', {
                "error": "enter username and password"
            })

        # Check the authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:

            # Log the user in
            login(request, user)

            # Redirect user to home page
            return redirect('index')
        else:

            # Show an error and redirect user to home page
            return render(request, 'home/login.html', {
                "error": "username and/or password is incorrect"
            })

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render(request, 'home/login.html')


def log_out(request):
    """Log user out"""

    # Forget any user_id
    logout(request)

    # Redirect user to login form
    return redirect('log_in')


def sell(request):
    """"Present a product for sale"""

    if request.method == "POST":
        return render(request, 'home/sell.html')
    else:
        return render(request, 'home/sell.html')


def buy(request):
    """"Present a product for purchase"""

    if request.method == "POST":
        return render(request, 'home/buy.html')
    else:
        return render(request, 'home/buy.html')
