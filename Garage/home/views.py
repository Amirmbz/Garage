from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password


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

        # Redirect user to home page
        return render(request, 'home/index.html')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render(request, 'home/register.html')


def signin(request):
    """Log user in"""

    # Forget any user_id
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
            return render(request, 'home/index.html')
        else:

            # Show an error and redirect user to home page
            return render(request, 'home/login.html', {
                "error": "enter username and password"
            })

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render(request, 'home/login.html')


def logout(request):
    """Log user out"""

    # Forget any user_id
    request.session.clear()

    # Redirect user to login form
    return redirect("home:index")
