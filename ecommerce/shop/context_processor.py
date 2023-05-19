from shop.models import Category, Wishlist



def default(request):
    categories = Category.objects.all()
    try:
      wishlist = Wishlist.objects.filter(user=request.user)
    except:
      wishlist = 0

    return {
      'categories': categories,
      'w': wishlist,
    }