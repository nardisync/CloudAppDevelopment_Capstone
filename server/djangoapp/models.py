from django.db import models
from django.utils.timezone import now

# Car Make model 
class CarMake(models.Model):
    name = models.CharField(null=False, 
            max_length=30, 
            default="Car Maker",
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

    car_maker   = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    car_name    = models.CharField(max_length=30, default="Car Name", 
                        null=False,primary_key=True )
    dealer_id   = models.IntegerField(null=False)
    car_type    = models.CharField(choices=CAR_TYPE, default='Sedan', max_length=50)
    car_year    = models.DateField()

    def __str__(self):
        return f"Car Model: {self.car_name} | Type: {self.car_type} | Maker: {self.car_maker}"\
                "Year of Production: {self.car_year}\nDealer ID: {self.dealer_id}"


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
