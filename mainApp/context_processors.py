from .models import Category
from datetime import datetime

def all_categories(request):
    categories = Category.objects.all()
    current_year = datetime.now().year
    return {'categories': categories,'current_year':current_year,}