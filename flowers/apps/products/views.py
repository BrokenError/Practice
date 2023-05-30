from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView

from apps.cart.forms import CartAddProductForm
from apps.orders.models import Order
from apps.products.forms import ReviewForm
from apps.products.models import Products, Rating, Reviews


def about_us(request):
    context = {'title': 'О нас'}
    return render(request, 'products/aboutus.html', context=context)


class ShowProduct(DetailView):
    model = Products
    template_name = 'products/product.html'
    slug_url_kwarg = 'prod_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShowProduct, self).get_context_data(**kwargs)
        product = get_object_or_404(Products, slug=self.kwargs['prod_slug'])
        user_orders = list(Order.objects.filter(user_id=self.request.user.id))
        context['stars'] = Rating.objects.filter(prod=product.id).aggregate(Avg('star')).get('star__avg')
        orderitems_id = []
        context['product_paid'] = False
        for order in user_orders:
            for order_item in list(order.linkorder.all()):
                orderitems_id.append(order_item.product_id)
        if product.id in orderitems_id and not \
                Reviews.objects.filter(user=self.request.user.id, product=product.id).exists():
            context['product_paid'] = True
        context.update({'product': product, 'comments': Reviews.objects.filter(product=product),
                        'star': [1, 2, 3, 4, 5], 'cart_product_form': CartAddProductForm()})
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
        form = ReviewForm(request.POST)
        product = Products.objects.get(id=pk)
        if form.is_valid():
            forme = form.save(commit=False)
            forme.user = request.user
            forme.product = product
            forme.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
