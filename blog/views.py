from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import NewsForm, CategoryForm, AuthorForm
from .models import *
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models.functions import Length
# Create your views here.


def index(request):
    latest_news = News.objects.all().order_by('-publish_date')[:4]
    news = News.objects.annotate(text_length=Length('title')).order_by('-text_length')[:3]
    long_title_news = News.objects.annotate(title_length=Length('title')).order_by('-title_length')[:4]
    categories_with_videos = []
    categories = Category.objects.all().order_by('id')[:2]  # faqat 2 ta kategoriya
    news_by_category = {
        cat: News.objects.filter(category=cat) for cat in categories
    }

    for category in Category.objects.all():
        # Faqat shu category'ga tegishli va videoga ega News larni olish
        news_with_video = category.news_set.exclude(video='').exclude(video__isnull=True)

        if news_with_video.exists():
            categories_with_videos.append({
                'category': category,
                'news': news_with_video
            })

    video_news = News.objects.exclude(video='')

    # Ushbu yangiliklarga tegishli bo‘lgan toifalar
    categories_with_video = Category.objects.filter(news__in=video_news).distinct()
    category = Category.objects.all()
    paginator = Paginator(category, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    news = News.objects.all()
    return render(request, 'index.html', {'news': news, 'category': category, 'page_obj': page_obj, 'video_news': video_news, 'categories_with_video': categories_with_video, 'categories_with_videos': categories_with_videos, 'long_title_news': long_title_news, 'news_by_category': news_by_category, 'news': news, 'latest_news': latest_news}) 

def video_news(request):
    videos = News.objects.filter(video__isnull=False).exclude(video='')
    return render(request, 'video_news.html', {'videos': videos})

def search_news(request):
    query = request.GET.get('q')  # "q" - bu formadagi input nomi
    if query:
        results = News.objects.filter(title__icontains=query)  # title bo'yicha qidiruv
    else:
        results = News.objects.all()  # Agar qidiruv so'rovi bo'lmasa, barcha yangiliklarni chiqarish

    return render(request, 'search.html', {'news': results})

def about(request):
    # author = Author.objects.all()
    author_info = Author.objects.first()  # Muallif haqida ma'lumot olish
    return render(request, 'about.html', {'author': author_info})


def category_news(request, pk):
    category = Category.objects.get(pk=pk)  # Kategoriyani olish
    news = News.objects.filter(category=category).order_by('-publish_date')  # Kategoriyaga mos yangiliklarni olish
    return render(request, 'category_news.html', {'category': category, 'news': news})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news_detail.html', {'news': news})


def information_list(request):
    context = {
        'presentations': Presentation.objects.all(),
        'help_guides': HelpGuide.objects.all(),
        'reports': OfficialDocument.objects.all()
    }
    # Ma'lumotlar ro'yxatini olish
    information = Information.objects.all()
    return render(request, 'informations.html', {'information': information, **context})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Siz tizimga muofoqiyatli kirdingiz.")
            return redirect("create_news")  # Tizimga kirgandan keyin qaysi sahifaga o'tish kerakligini ko'rsatish
        else:
            messages.error(request, "User va parol xato yoki bunday user mavjud emas.")

    return render(request, 'login.html')

@login_required
def edit_author(request):
    author = get_object_or_404(Author, pk=1)  # faqat bitta (masalan pk=1) muallifni tahrirlash

    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            return redirect('about')  # tahrirlangandan so‘ng redirect
    else:
        form = AuthorForm(instance=author)

    return render(request, 'create_author.html', {'form': form})

@login_required
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = NewsForm()
    categories = Category.objects.all()
    return render(request, 'news_create.html', {'form': form, 'categories': categories})

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to a category list page or any other page
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})


@login_required  # faqat autentifikatsiyalangan foydalanuvchilar uchun
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)  # Foydalanuvchi faylni yuborgan bo'lsa, request.FILES kerak
        if form.is_valid():
            form.save()
            return redirect('index')  # Yangi yangilikni qo'shgandan keyin boshqa sahifaga o'tish
    else:
        form = NewsForm()

    categories = Category.objects.all()  # Barcha kategoriyalarni olish
    return render(request, 'post.html', {'form': form, 'categories': categories})  # Yangilik qo'shish sahifasini ko'rsatish


# def login_view(request):
#     if request.method == 'POST':  # Agar POST so‘rovi bo‘lsa
#         form = LoginForm(request.POST)  # Formani POST ma'lumotlari bilan yaratish
#         if form.is_valid():  # Forma validatsiya qilinganini tekshirish
#             username = request.POST.get('username')  # Foydalanuvchi nomini olish
#             password = request.POST.get('password')  # Parolni olish
#             user = authenticate(request, username=username, password=password)  # Foydalanuvchini autentifikatsiya qilish
#             if user is not None:
#                 login(request, user)  # Foydalanuvchini tizimga kiritish
#                 return redirect('index')  # Home sahifasiga yo‘naltirish
#             else:
#                 messages.error(request, 'Foydalanuvchi nomi yoki parol noto‘g‘ri!')
#     else:  # Agar GET so‘rovi bo‘lsa
#         form = LoginForm()  # Yangi forma yaratish

#     return render(request, 'login.html', {'form': form})  

def logout_view(request):
    logout(request)
    return redirect('index')  # Logoutdan so‘ng login sahifasiga yo‘naltirish

