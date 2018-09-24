from cart.cart import Cart


def cart(request):
    return {'cart': Cart(request)}

# A context processor is a python function that takes request object as an argument and return the dictionary that
# get added to the request context. That makes handy when you need to make something available to all page like
# add to card.
