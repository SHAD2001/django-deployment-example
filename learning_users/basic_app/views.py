from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm


from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request,'basic_app/index.html')


def special(request):
    return HttpResponse('You are logged in, nice!')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))




def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            # Update with Hashed password
            user.save(user.set_password(user.password))




            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'basic_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})


@login_required
def user_view(request):
    return render(request,'basic_app/users_page.html')




def user_login(request):

    if request.method == 'POST':
        # Getting from login html
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)


        if user:
            # if user.is_activate:
                login(request,user)
                return HttpResponse(user_view(request))
            # else:
            #     return HttpResponse('ACCOUNT NOT ACTIVATE')
        else:
            print('Some one tried to login and failde')
            print('Username: {} and password {}'.format(username,password))
            return  HttpResponse('Invalid Login details supplied')
    else:
        return render(request,'basic_app/login.html')
