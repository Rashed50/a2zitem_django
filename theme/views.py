from django.shortcuts import render, redirect

def home(request):
    return render(request, "base.html")

def toggle_theme(request):
    is_dark = request.session.get("is_dark", False)
    print("-----------------------")
    print("is_dark:", is_dark)
    print("-----------------------")
    request.session["is_dark"] = not is_dark
    request.session.modified = True
    return redirect("home")
