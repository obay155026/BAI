from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from re import split
from Reg._8puzzle import bestsolution, evaluvate, evaluvate_misplaced
# Create your views here.

path_moves = None
total_moves = 0


def solve(initial_pieces, final_pieces):
    global total_moves
    global path_moves
    global processing
    if(initial_pieces != final_pieces):
        state, visited = evaluvate(initial_pieces, final_pieces)
        print(state)
        print(visited)
        best_path = bestsolution(state)
        total_moves = len(best_path) - 1
        path_moves = [None] * (total_moves + 1)
        for step in range(total_moves+1):
            pieces = split('', str(best_path[step]).replace(
                '[', '').replace(']', '').replace('\n', '').replace(' ', ''))
            pieces = list(filter(lambda a: a != '', pieces))
            path_moves[step] = pieces
    else:
        path_moves = None


processing = False


def index(request):
    global processing
    global path_moves
    initial_state_pieces = []
    final_state_pieces = []
    path_moves = None
    if request.method == 'POST':
        if(not processing):
            processing = True
            # Extract the initial state numbers from the hidden fields
            for i in range(9):
                val = request.POST.get('initStatePiece_{}'.format(i))
                initial_state_pieces.append(0 if val == '' else int(val))

            # Extract the final state numbers from the text fields
            for i in range(9):
                val = request.POST.get('finalStatePiece_{}'.format(i))
                final_state_pieces.append(0 if val == '' else int(val))

            solve(initial_state_pieces, final_state_pieces)
            processing = False

    return render(request, 'home.html', {'range': range(0, 9), 'path_moves': path_moves, 'total_moves': total_moves})


@login_required(login_url='login')
def HomePage(request):
    return render(request,'home.html')
def SinupPage(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        username = request.POST.get('username')

        if pass1 != pass2:
            return HttpResponse("Passwords doesn't match")
        else:
            my_user = User.objects.create_user(fname, username, pass1)
            my_user.save()
            return redirect("login")
            print (uname, email, pass1, pass2)
    return render(request,'Reg.html')
def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request, username=username ,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")
    return render(request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')