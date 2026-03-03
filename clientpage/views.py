from django.shortcuts import render
from django.views import View
from apps.product.models.category import Category
from apps.product.models.brand import Brand

# Create your views here.
class ClintPageView(View):
    def get(self, request):
        # context = {
        #     'featured_categories': Category.objects.filter(parent__isnull=True)[:6],
        #     'popular_brands': Brand.objects.all()[:8],
        # }
        # return render(request, "clintpage/home.html")
        return render(request, "clintpage/home2.html")