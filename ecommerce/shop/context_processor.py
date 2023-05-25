from shop.models import Category, Wishlist, Banner



def default(request):
    categories = Category.objects.all()

    try:
      wishlist = Wishlist.objects.filter(user=request.user)
    except:
      wishlist = 0
 
    if wishlist != 0:
        totalwishlistitems = wishlist.count()
    else:
        totalwishlistitems = wishlist

    
    banner = Banner.objects.filter(draft=False).first()

    return {
      'categories': categories,
      'w': wishlist,
      'totalwishlistitems': totalwishlistitems,
      'banner': banner,
    }