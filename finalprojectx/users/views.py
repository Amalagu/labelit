from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views import generic
from django.http import HttpResponseRedirect
from .models import Profile
from .forms import CustomUserCreationForm, AuthForm, ProjectForm
from label.models import Project, ImageSample
from django.contrib import messages

# Create your views here.
def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('index-view')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'index-view')

        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'users/login_register.html')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('index-view')

        else:
            messages.success(
                request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

"""
class LoginView(generic.FormView):
    form_class = AuthForm
    template_name = "users/signin.html"
    success_url = ''

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())
"""

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')








#@login_required(login_url = 'login')
def index(request):
    context = {}
    if hasattr(request.user, 'profile'):
        #if request.user.profile:
        profile = request.user.profile
        projects = profile.project_set.all()
        annotationprojects = profile.annotationprojects.all()
        #projects = projects.union(annotationprojects)
        context = {"projects": projects, 'annotationprojects': annotationprojects}
    else:
        pass
    #print(dir(request.user.profile))
    return render(request, 'base/index.html', context)

@login_required(login_url='login')
def projectimages(request, pk):
    project = Project.objects.get(id=pk)
    context = {'project':project}
    return render(request, 'label/project-images.html', context)

@login_required(login_url='login')
def singleimages(request, pk):
    email = request.user.profile.email
    image = ImageSample.objects.get(id=pk)
    imagedict = image.imagedata[email].items() or {"Texture":' ', "Gradient":'', "Age":' ', "Other Symptoms":''}
    if request.method == 'POST':
        for x,y in imagedict:
            value = request.POST.get(x)
            image.imagedata[email][x] = value
        image.save()
        return redirect('index-view')
    context = {'image':image, 'imagedata': imagedict}
    return render(request, 'label/single-image.html', context)

@login_required(login_url='login')
def labelimage(request, pk):
    if request.method == 'POST':
        pass
    return

@login_required(login_url='login')
def useraccount(request):
    profile = request.user.profile
    print(dir(profile))
    context = {'profile': profile}
    return render(request, 'users/account.html', context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        annotators = request.POST.get('annotators').replace(',',  " ").split()
        images = request.FILES.getlist('images')
        initial_image_data = {}


        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for annotator_email in annotators:
                try:
                    annotator = Profile.objects.get(email=annotator_email)
                    project.annotators.add(annotator)
                    initial_image_data[annotator_email] = {"Texture":' ', "Gradient":'', "Age":' ', "Other Symptoms":''}
                except:
                    pass
            for image in images:
                try:
                    new_image = ImageSample.objects.create(featured_image=image, imagedata=initial_image_data)
                    project.featured_image.add(new_image)
                except:
                    pass


            return redirect('account')

    context = {'form': form, 'project': project}
    return render(request, "label/project-form.html", context)

def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        annotators = request.POST.get('annotators').replace(',',  " ").split()
        images = request.FILES.getlist('images')


        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            for annotator in annotators:
                try:
                    annotator = Profile.objects.get(email=annotator)
                    project.annotators.add(annotator)
                except:
                    pass
            for image in images:
                try:
                    new_image = ImageSample.objects.create(featured_image=image)
                    project.featured_image.add(new_image)
                except:
                    pass
            project.manager=profile
            project.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'label/project-form.html', context)



@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context = {'object': project}
    return render(request, 'base/delete-template.html', context)


