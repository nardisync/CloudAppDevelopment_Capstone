from django.db import models
from django.utils.timezone import now

# Car Make model 
class CarMake(models.Model):
    name = models.CharField(null=False, 
            max_length=30,
            primary_key=True)
    description = models.TextField()

    def __str__(self):
        return f"Car Maker: {self.name} \nDescription: {self.description}" 



# Car Model model 
class CarModel(models.Model):
    CAR_TYPE = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('CROSSOVER', 'Crossover'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
        ('HATCHBACK', 'Hatchback')
    ]
    car_id      = models.AutoField(primary_key=True)
    car_maker   = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    car_name    = models.CharField(max_length=30, default="Car Name", 
                        null=False)
    dealer_id   = models.IntegerField(null=False)
    car_type    = models.CharField(choices=CAR_TYPE, default='Sedan', max_length=50)
    car_year    = models.DateField()

    def __str__(self):
        return f"Car ID: {self.car_id} | Car Model: {self.car_name} | Type: {self.car_type} | Maker: {self.car_maker} \nYear of Production: {self.car_year}\nDealer ID: {self.dealer_id}"


# A Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# A Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review, sentiment, id, purchase_date = None, car_make=None, 
                    car_model=None, car_year=None):
        # Dealership
        self.dealership = dealership
        # Dealership name
        self.name = name
        # Dealership purchase | Boolean
        self.purchase = purchase
        # Review
        self.review = review
        # Purchase Date
        self.purchase_date = purchase_date
        # Car Make
        self.car_make = car_make
        # Car Model 
        self.car_model = car_model
        # Car Year
        self.car_year = car_year
        # Sentiment of the review
        # Positive | Neutral | Negative
        self.sentiment = sentiment
        # Review ID
        self.id = id

    def __str__(self):
        return "DealerReview: " + self.review + "\nReview Sentiment: " + self.sentiment