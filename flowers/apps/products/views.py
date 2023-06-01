from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView

from apps.cart.forms import CartAddProductForm
from apps.orders.models import Order
from apps.products.forms import ReviewForm, CommentForm
from apps.products.models import Products, Rating, Reviews, Comments


def about_us(request):
    context = {'title': 'О нас'}
    return render(request, 'products/aboutus.html', context=context)


class BaseProduct(DetailView):
    slug_url_kwarg = 'prod_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Products, slug=self.kwargs['prod_slug'])
        user_orders = Order.objects.filter(user_id=self.request.user.id)
        context['stars'] = Rating.objects.filter(prod=product.id).aggregate(Avg('star')).get('star__avg')
        context['product_paid'] = False
        check_buy = user_orders.filter(linkorder__product_id=product.id)
        check_not_review = not Reviews.objects.filter(user=self.request.user.id, product=product.id).exists()
        if check_buy:
            context['product_paid'] = True
        context.update({'product': product, 'star': [1, 2, 3, 4, 5],
                        'cart_product_form': CartAddProductForm(), 'check_not_review': check_not_review})
        return context


class ShowReviewsView(BaseProduct):
    model = Products
    template_name = 'products/reviews.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_new = super(BaseProduct, self).get_context_data(**kwargs)
        context.update(context_new)
        context.update({'reviews': Reviews.objects.filter(product=context['product'].id)})
        return context


class ShowCommentsView(BaseProduct):
    model = Products
    template_name = 'products/comments.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_new = super(BaseProduct, self).get_context_data(**kwargs)
        context.update(context_new)
        context.update({'comments': Comments.objects.filter(product=context['product'].id)})
        return context


def grade_product(request):
    grade = request.GET.get('grade_product')
    user_grade = str(grade).split()
    prod = Products.objects.get(id=user_grade[1])
    update_for = {'user': request.user, 'star': user_grade[0], 'prod': prod}
    Rating.objects.update_or_create(user=request.user, defaults=update_for)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddReviews(View):

    def post(self, request, pk):
        print('!!')
        form = ReviewForm(request.POST)
        product = Products.objects.get(id=pk)
        if form.is_valid():
            print('!!!!!!!!!!!!!!!!!!!!!')
            forme = form.save(commit=False)
            forme.user = request.user
            forme.product = product
            forme.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddComments(View):

    def post(self, request, pk):
        form = CommentForm(request.POST)
        product = Products.objects.get(id=pk)
        if form.is_valid():
            forme = form.save(commit=False)
            forme.user = request.user
            forme.product = product
            forme.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    