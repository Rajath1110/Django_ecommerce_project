from django.shortcuts import render,redirect
from .models import Product,Category
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm

# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products':products})

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})

def category(request, category_name):
    category_name = category_name.replace('-', ' ')
    try:
        # Fetch the specific category
        category = Category.objects.get(name=category_name)
        
        # Fetch only the products belonging to the specific category
        products = Product.objects.filter(category=category)
        
        return render(request, 'category.html', {'products': products, 'category': category})
    except Category.DoesNotExist:
        messages.error(request, "Category does not exist")
        return redirect('home')

        


def about(request):
    return render(request,'about.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('home')
        else:
            messages.error(request, "Wrong credentials, try again")  # Use error for wrong credentials
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('home')



def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Account created successfully")
                return redirect('home')
        else:
            messages.error(request, "Error while creating account, please try again")
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})
