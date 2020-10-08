from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
# Importa los modelos de bbdd de rango
from django.template import RequestContext

from rango.models import Category, Page, UserProfile
# Importa los modelos de formularios
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
# Importa preferencias de login, autenticación
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
# Importa preferencias de acceso login, cerrarsession
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.shortcuts import redirect


def index(request):
    if request.session.get('last_visit'):
        # The session has a value for the last visit
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', 0)

        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())
    else:
        # The get returns None, and the session does not have a value for the last visit.
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1
    #### END NEW CODE ####

    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages_views': pages_list}
    for category in category_list:
        category.url = category.name.replace(' ', '_')

    cat_list = get_category_list()
    context_dict['cat_list'] = cat_list

    return render(request, 'rango/index.html', context_dict)


def about(request):
    if request.session.get('visits'):
        visits = request.session.get('visits', 0)
        request.session['visits'] = visits + 1
    else:
        request.session['visits'] = 1

    count = request.session.get('visits')
    return render(request, 'rango/about.html', {'visits': count})


def category(request, category_name_url):
    cat_list = get_category_list()
    category_name = decode_url(category_name_url)
    context_dict = {'cat_list': cat_list, 'category_name': category_name}
    try:
        category = Category.objects.get(name=category_name)
        context_dict['category'] = category

        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})


def get_category_list():
    cat_list = Category.objects.all()

    for cat in cat_list:
        cat.url = encode_url(cat.name)

    return cat_list


def add_page(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = PageForm()
    return render(request, 'rango/add_page.html', {'form': form})


def decode_url(category_name_url):
    category_name = category_name_url.replace('_', ' ')
    return category_name


def encode_url(category_name):
    category_name_url = category_name.replace(' ', '_')
    return category_name_url


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
                  'rango/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'rango/login.html', {})


def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are logged in.")
    else:
        return HttpResponse("You are not logged in.")


def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)


def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__startswith=starts_with)
    else:
        cat_list = Category.objects.all()

    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]

    for cat in cat_list:
        cat.url = encode_url(cat.name)

    return cat_list


def suggest_category(request):
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    else:
        starts_with = request.POST['suggestion']

        cat_list = get_category_list(8, starts_with)

    return render(request,'rango/category_list.html', {'cat_list': cat_list})


@login_required
def profile(request):
    cat_list = get_category_list()
    context_dict = {'cat_list': cat_list}
    u = User.objects.get(username=request.user)

    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render(request, 'rango/profile.html', context_dict)


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')

@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        category = Category.objects.get(id=int(cat_id))

        if category:
            likes = category.likes + 1
            category.likes = likes
            category.save()

    return HttpResponse(likes)



