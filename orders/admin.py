import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe


def export_to_csv(modeladmin, request, queryset):
    """
    1.You create an instance of HttpResponse, specifying the text/csv content type, to tell the
        browser that the response has to be treated as a CSV file. You also add a Content-Disposition
        header to indicate that the HTTP response contains an attached file.

    2.You create a CSV writer object that will write to the response object.
    
    3.You get the model fields dynamically using the get_fields() method of the model’s _meta
        options. You exclude many-to-many and one-to-many relationships.
    
    4.You write a header row including the field names.
    
    5.You iterate over the given QuerySet and write a row for each object returned by the QuerySet.
        You take care of formatting datetime objects because the output value for CSV has to be a string.
    
    6.You customize the display name for the action in the actions drop-down element of the admin-
        istration site by setting a short_description attribute on the function.
    """
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'
                

# Inline allows you to include a models
# on the same edit page as its related model. 

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''
order_payment.short_description = 'Stripe payment'

@admin.register(Order)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    order_payment,
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInLine]
    actions = [export_to_csv]