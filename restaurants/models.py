from django.db    import models

class Restaurant(models.Model):
    name               = models.CharField(max_length=45)
    address            = models.CharField(max_length=100)
    phone_number       = models.CharField(max_length=50, null=True)
    locations_id       = models.ForeignKey('Location',on_delete=CASCADE, db_column='locations_id')
    categories_id      = models.ForeignKey('Category', on_delete=CASCADE, db_column='categories_id')
    serving_prices_id  = models.ForeignKey('ServingPrice', on_delete=CASCADE, db_column='serving_prices_id')

    class Meta:
        db_table = 'restaurants'

class Menu(models.Model):
    restaurants_id = models.ForeignKey('Restaurant', on_delete=CASCADE, db_column='restaurants_id')
    item           = models.CharField(max_length=45)
    item_price     = models.DecimalField(max_digits= 6, decimal_places=0)

    class Meta:
        db_table = 'menus'

class Location(models.Model):
    area = models.CharField(max_length=45)

    class Meta:
        db_table = 'locations'

class Category(models.Model):
    kind = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class ServingPrice(models.Model):
    price = models.CharField(max_length=45)

    class Meta:
        db_table = 'serving_prices'