from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(User):
    # customer_id = models.CharField(primary_key=True,max_length=128)
    # first_name = models.CharField(max_length=128)
    # last_name = models.CharField(max_length=128)
    # pass_word = models.CharField(max_length=256)


    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

class Employee(User):
    # customer_id = models.CharField(primary_key=True,max_length=128)
    # first_name = models.CharField(max_length=128)
    # last_name = models.CharField(max_length=128)
    # pass_word = models.CharField(max_length=256)


    class Meta:
        verbose_name = '雇员'
        verbose_name_plural = '雇员'

class Bus(User):

    bus_id = models.AutoField(primary_key=True)
    bus_name = models.CharField(max_length=128)
    class Meta:
        verbose_name = '车'
        verbose_name_plural = '车'


class Bus_driver(User):

    # driver_id = models.CharField(primary_key=True,max_length=128)
    # first_name = models.CharField(max_length=128)
    # last_name = models.CharField(max_length=128)
    # pass_word = models.CharField(max_length=256)
    bus = models.ForeignKey(Bus, models.DO_NOTHING)

    class Meta:
        verbose_name = '司机'
        verbose_name_plural = '司机'



class Route(models.Model):

    Route_id = models.AutoField(primary_key=True)
    Route_name = models.CharField(max_length=128)

    class Meta:
        verbose_name = '线路'
        verbose_name_plural = '线路'


class Station(models.Model):

    station_id = models.AutoField(primary_key=True)
    station_name = models.CharField(max_length=128)
    price = models.IntegerField()
    route_id = models.ForeignKey(Route, models.DO_NOTHING)

    class Meta:
        verbose_name = '站点'
        verbose_name_plural = '站点'


class Shuttle(models.Model):


    shuttle_id = models.AutoField(primary_key=True)
    route_id = models.ForeignKey(Route, models.DO_NOTHING)
    direction = models.CharField(max_length=128)
    departure_time = models.DateTimeField()
    driver_id = models.ForeignKey(Bus_driver, models.DO_NOTHING)

    class Meta:
        verbose_name = '班次'
        verbose_name_plural = '班次'


class Order(models.Model):

    order_id = models.AutoField(primary_key=True)
    station_id = models.ForeignKey(Station, models.DO_NOTHING)
    shuttle_id = models.ForeignKey(Shuttle, models.DO_NOTHING)
    customer_id = models.ForeignKey(Customer, models.DO_NOTHING)
    number = models.IntegerField()

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'

class Ticket(models.Model):

    ticket_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, models.DO_NOTHING)
    seat_id = models.IntegerField()
    validate = models.BooleanField(default=False)

    class Meta:
        verbose_name = '票'
        verbose_name_plural = '票'

class Payment(models.Model):

    payment_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, models.DO_NOTHING)
    payment = models.IntegerField()

    class Meta:
        verbose_name = '交易记录'
        verbose_name_plural = '交易记录'
