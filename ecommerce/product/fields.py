from django.db import models
from django.core import checks
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    """We are buidling a new custom field"""
    
    description = "Ordering field on a unique field"

    def __init__(self, unique_for_field=None, *args, **kwargs):
        self.unique_for_field = unique_for_field
        super().__init__(*args, **kwargs)


    def check(self, **kwargs):
        """I used docs for CharField and IntegerField to have an idea of how to write this"""
        return [
            *super().check(**kwargs),
            *self._check_for_field_attribute(**kwargs),
        ]
    
    def _check_for_field_attribute(self, **kwargs):
        if self.unique_for_field is None:
            return [
                checks.Error("OrderField must define a 'unique_for_field' attribute"),
                    ]
        elif self.unique_for_field not in [f.name for f in self.model._meta.get_fields()]:
            """Checking if the field name provided is not defined in our model"""
            return [
                checks.Error("OrderField entered does not match an existing model field"),
                    ]
        else:
            return []
        

    def pre_save(self, model_instance, add):
        """Every/Each instance of order number created passes/passed through the pre_save function here"""
        # print(model_instance)
        if getattr(model_instance, self.attname) is None:
            """When no order number value is inputed,
              If there is no order number value inputed, then we would need to generate one."""
            qs = self.model.objects.all() #self.model ProductLine model
            # ' Select * from ProductLine where product="shoe" '
            try: # Build your query to filter out all of the Product-Line that belongs to a specific product
                query = {
                    self.unique_for_field: getattr(model_instance, self.unique_for_field) 
                    }# {"product": "Nike shoe"}
                qs = qs.filter(**query) # print(query)  # print(qs)
                last_item = qs.latest(self.attname) #self.attname == order #latest gets the last item
                value = last_item.order+1
            except ObjectDoesNotExist: #If no data in the database, then value = 1, first value
                value = 1
            return value #This saves directly to the order field in the db, #order = OrderField(unique_for_field="product" , blank=True)
        else:
            return super().pre_save(model_instance, add)
        
        
