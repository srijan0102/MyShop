from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):

    def __init__(self, request):
        """
        initialize the cart
        """
        self.session = request.session  # store current session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = dict()  # if no cart is present then we set empty cart
        self.cart = cart

    def __len__(self):
        """
        Count all items in the cart
        :return:
        """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        Iterate over items in the cart and get the product from database.
        :return:
        """
        product_ids = self.cart.keys()
        # get the product object and add them to the cart
        products = Product.objects.filter(id__in=product_ids)  # do not use category_id__in
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price']*item['quantity']
            yield item

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add product to the cart or update its quantity.
        :param product:
        :param quantity:
        :param update_quantity:
        :return:
        """
        product_id = str(product.id)  # because django usage json to serialize data and json allows string name
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Save and bring update in the cart
        :return:
        """
        self.session[settings.CART_SESSION_ID] = self.cart  # Update the session cart
        self.session.modified = True  # mark the session as modified to make sure it is saved

    def clear(self):
        """
        Empty the cart
        :return:
        """
        self.session[settings.CART_SESSION_ID] = dict()
        self.session.modified = True

    def remove(self, product):
        """
        Remove a Product from the cart
        :return:
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """
        Get Total price of items.
        :return:
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


