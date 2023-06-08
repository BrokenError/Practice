from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import register
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
        context['check_like'] = product.check_like.filter(user=self.request.user, product=product).exists()
        check_buy = user_orders.filter(linkorder__product_id=product.id)
        check_not_review = not product.check_review.filter(user=self.request.user.id).exists()
        if check_buy:
            context['product_paid'] = True
        context.update({'product': product, 'star': [1, 2, 3, 4, 5],
                        'cart_product_form': CartAddProductForm(), 'check_not_review': check_not_review})
        return context


@register.filter
def filter_user(req, user):
    return req.filter(user=user)


class ShowReviewsView(BaseProduct):
    model = Products
    template_name = 'products/reviews.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_new = super(BaseProduct, self).get_context_data(**kwargs)
        context.update(context_new)
        context.update({'reviews': Reviews.objects.filter(product=context['product'].id).order_by('-date_uploaded')})
        return context


class ShowCommentsView(BaseProduct):
    model = Products
    template_name = 'products/comments.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_new = super(BaseProduct, self).get_context_data(**kwargs)
        context.update(context_new)
        context.update({'comments': Comments.objects.filter(product=context['product'].id).order_by('-date')})
        return context
    

def grade_product(request):
    grade = request.GET.get('grade_product')
    user_grade = str(grade).split()
    prod = Products.objects.get(id=user_grade[1])
    update_for = {'user': request.user, 'star': user_grade[0], 'prod': prod}
    Rating.objects.update_or_create(user=request.user, defaults=update_for)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddReviews(View):

    @staticmethod
    def post(request, pk):
        form = ReviewForm(request.POST)
        product = Products.objects.get(id=pk)
        if form.is_valid():
            forme = form.save(commit=False)
            forme.user = request.user
            forme.product = product
            forme.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddComments(View):

    @staticmethod
    def post(request, pk):
        form = CommentForm(request.POST)
        product = Products.objects.get(pk=pk)
        if form.is_valid():
            forme = form.save(commit=False)
            forme.user = request.user
            forme.product = product
            forme.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_review(request, pk):
    Reviews.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_comment(request, pk):
    Comments.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def change_review(request, product_id, review_id):
    change(request, product_id, review_id, Reviews, ReviewForm, 0)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def change(request, product_id, check_id, model, check_form, check_reply):
    form = check_form(request.POST)
    form.save(commit=False)
    check_write = model.objects.filter(id=check_id).filter(product_id=product_id)
    if check_write.exists() and model == Reviews:
        check_write.update(text=form.cleaned_data['text'], name=form.cleaned_data['name'])
    elif check_write.exists() and model == Comments:
        check_write.update(text=form.cleaned_data['text'])
    elif check_reply != 0:
        check_write = check_write.filter(comment_id=check_reply)
        check_write.update(text=form.cleaned_data['text'])
    return False


def change_comment(request, product_id, comment_id):
    change(request, product_id, comment_id, Comments, CommentForm, 0)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
