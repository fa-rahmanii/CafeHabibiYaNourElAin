from django.contrib import admin
from .models import Product, Storage, Order, OrderProduct, Category, ProductIngredient, SliderItem
from django.urls import path
from django.shortcuts import render
from django.db.models import Sum
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.


class CustomAdminSite(admin.AdminSite):
    site_header = 'Coffee Shop Administration'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sales-chart/', self.admin_view(self.sales_chart_view), name='sales_chart'),
        ]
        return custom_urls + urls

    def sales_chart_view(self, request):
        interval = request.GET.get('interval', 'monthly')

        if interval == 'daily':
            sales_data = OrderProduct.objects.values('product__name').annotate(total_quantity=Sum('quantity')).order_by('product__name')
        elif interval == 'weekly':
            sales_data = OrderProduct.objects.values('product__name').annotate(total_quantity=Sum('quantity')).order_by('product__name')
        else:
            sales_data = OrderProduct.objects.values('product__name').annotate(total_quantity=Sum('quantity')).order_by('product__name')

        context = {
            'sales_data': sales_data,
            'interval': interval,
        }
        return render(request, 'shop/sales_chart.html', context)

admin_site = CustomAdminSite(name='custom_admin')
admin.site = admin_site


class ProductIngredientInline(admin.TabularInline):
    model = ProductIngredient
    extra = 1  

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductIngredientInline]
    list_display = ('name', 'category', 'price')
    search_fields = ('name',)
    list_filter = ('category',)
    def view_sales_chart(self, obj):
        return format_html('<a class="button" href="{}">View Sales Chart</a>',
            reverse('sales_chart')
        )
    view_sales_chart.short_description = 'Sales Chart'
    view_sales_chart.allow_tags = True



admin.site.register(Storage)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Category)
admin.site.register(SliderItem)
