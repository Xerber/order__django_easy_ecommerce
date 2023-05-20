from shop.models import Category, Wishlist, Banner



def default(request):
    categories = Category.objects.all()

    try:
      wishlist = Wishlist.objects.filter(user=request.user)
    except:
      wishlist = 0
    
    banner = Banner.objects.filter(draft=False).first()

    return {
      'categories': categories,
      'w': wishlist,
      'banner': banner,
    }