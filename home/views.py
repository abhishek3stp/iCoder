from django.shortcuts import render, redirect
from home.models import Contact
from blog.models import Post
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Home page
def home(request):
    allPosts = Post.objects.all().order_by('-sno')[:3]
    params = {'allPosts': allPosts}
    return render(request, 'home/home.html', params)


# Contact page
def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        # Check whether this is a genuine contact request
        if len(name) < 5 or len(email) < 5 or len(phone) < 10 or len(content) < 5:
            messages.error(request, 'Please fill the form correctly.')
        
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, 'Your form submitted successfully, we will contact you soon.')
        
    return render(request, 'home/contact.html')


# About page
def about(request):
    return render(request, 'home/about.html')


# For searching the blog by title, author or content
def search(request):
    query = request.GET['query']

    # If searching string is very larger
    if len(query) > 75:
        allPosts = Post.objects.none()
    
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsAuthor, allPostsContent)
    
    # When there is search result found
    if allPosts.count() == 0:
        messages.warning(request, 'No search results found please refine your query.')
        
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)


# Handling the signin request
def handleSignup(request):
    if request.method=='POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check for errorneous inputs
        # Check for length of username should be under 15 char
        if len(username) > 15:
            messages.error(request, 'Username must be under 15 characters.')
            return redirect('home')

        # Check for alphanumeric username
        if not username.isalnum():
            messages.error(request, 'Username should only contain letters and numbers.')
            return redirect('home')

        # Password should be matched
        if password1 != password2:
            messages.error(request, 'Your confirm password not matched.')
            return redirect('home')
        
        # Ceate User
        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Your iCoder account has been successfully created.')
        return redirect('home')

    else:
        return HttpResponse("404 - Page not found")


# Handling the login request
def handleLogin(request):
    if request.method=='POST':
        usernamelogin = request.POST['usernamelogin']
        passwordlogin = request.POST['passwordlogin']

        # Authentication
        user = authenticate(username = usernamelogin, password = passwordlogin)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are successfully logged in.')
            return redirect('home')

        else:
            messages.error(request, 'Please enter correct login credentials.')
            return redirect('home')

    else:
        return HttpResponse("404 - Page not found")


# Handling logout
def handleLogout(request):
    logout(request)
    messages.success(request, 'You are successfully logged out.')
    return redirect('home')
