from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View
from .forms import ProductForm, ProductModeratorForm
from .models import Product, Contacts




def home(request):
    return render(request, template_name="home.html")


def contacts(request):
    return render(request, template_name="contacts.html")


class UnpublishProductView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if not request.user.has_perm("can_unpublish_product"):
            return HttpResponseForbidden("Вы не можете убирать товар")

        product.published_status = request.POST.get("published_status")
        product.save()

        return redirect("category:product_detail", pk=product_id)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_moderator"] = self.request.user.groups.filter(name="Модератор продуктов").exists()
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if request.user != product.owner and not request.user.groups.filter(name="Модератор продуктов").exists():
            return HttpResponseForbidden("У вас нет прав для редактирования этого продукта.")
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("product.can_unpublish_product"):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if request.user != product.owner and not request.user.groups.filter(name="Модератор продуктов").exists():
            return HttpResponseForbidden("У вас нет прав для удаления этого продукта.")
        return super().dispatch(request, *args, **kwargs)


class ContactsView(CreateView):
    model = Contacts
    fields = ['name', 'message']
    template_name = 'catalog/contacts.html'
    success_url = reverse_lazy('catalog:product_list')
