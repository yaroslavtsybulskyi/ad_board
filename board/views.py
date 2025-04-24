from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from board.models import Ad, Category, Comment, UserProfile


def home_view(request: HttpRequest) -> HttpResponse:
    """
    Home page view.
    :param request: the request object
    :return: rendered home page with last month's ad count
    """
    last_month_ads_count = Ad.get_ads_last_month().count()
    return render(request, 'board/home.html', {'last_month_ads_count': last_month_ads_count})


def view_all_ads(request: HttpRequest) -> HttpResponse:
    """
    Lists all ads with filtering, search, and sorting functionality.
    :param request: request object.
    :return: rendered list of all ads with filtering, search, and sorting functionality.
    """
    ads = Ad.objects.all()
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    category_id = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if price_min:
        ads = ads.filter(price__gte=price_min)
    if price_max:
        ads = ads.filter(price__lte=price_max)
    if category_id:
        ads = ads.filter(category_id=category_id)
    if date_from:
        ads = ads.filter(created_at__date__gte=date_from)
    if date_to:
        ads = ads.filter(created_at__date__lte=date_to)

    search_query = request.GET.get('q')
    if search_query:
        ads = ads.filter(title__icontains=search_query)

    sort_by = request.GET.get('sort')
    if sort_by in ['price', '-price', 'created_at', '-created_at']:
        ads = ads.order_by(sort_by)

    categories = Category.objects.all()
    return render(request, 'board/ad_view.html', {
        'ads': ads,
        'categories': categories,
        'request': request,
    })


def category_view(request: HttpRequest) -> HttpResponse:
    """
    Category view page.
    :param request: request object.
    :return: rendered category page with all categories
    """
    categories = Category.objects.all()
    return render(request, 'board/category_view.html', {'categories': categories})


def category_by_id_view(request: HttpRequest, category_id: int) -> HttpResponse:
    """
    Single category view page.
    :param request: http request object.
    :param category_id: id of category.
    :return: rendered category page with single category
    """
    category = get_object_or_404(Category, id=category_id)
    ads = Ad.get_active_ads_in_category(category.name)
    context = {'category': category, 'ads': ads}
    return render(request, 'board/category_by_id.html', context)


def view_ad_by_id(request: HttpRequest, ad_id: int) -> HttpResponse:
    """
    Single ad view page.
    :param request: http request object.
    :param ad_id: ad id
    :return: rendered ad page with info about specific ad
    """
    ad = get_object_or_404(Ad, id=ad_id)
    comments = Comment.objects.filter(ad=ad)
    total_comments = comments.count()

    context = {'ad': ad, 'comments': comments, 'total_comments': total_comments}
    return render(request, 'board/ad_view_by_id.html', context)


def users_view(request: HttpRequest, user_id: int) -> HttpResponse:
    """
    Users view page.
    :param request: request object.
    :param user_id: id of the user
    :return: rendered user page with info about user
    """
    user = get_object_or_404(User, id=user_id)
    user_profile, created = UserProfile.objects.get_or_create(user=user, defaults={'email': user.email})
    user_ads = Ad.objects.filter(user=user_profile)
    total_ads = user_ads.count()
    total_comments = Comment.objects.filter(user=user).count()

    context = {'user_profile': user_profile, 'user_ads': user_ads,
               'total_ads': total_ads, 'total_comments': total_comments}

    return render(request, 'board/users_view.html', context)
