import factory
import factory.fuzzy
import orders



class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = orders.models.Order

    created_on = factory.Faker('date_time')
    order_id = factory.fuzzy.FuzzyInteger(1)
    domain = factory.Faker('domain_name')
    price = factory.fuzzy.FuzzyDecimal(0)
    data = {}


class OrderDictFactory(factory.Factory):
    class Meta:
        model = dict

    created_on = '2006-10-25 14:30:59'
    order_id = factory.fuzzy.FuzzyInteger(1)
    domain = factory.Faker('domain_name')
    price = 25
