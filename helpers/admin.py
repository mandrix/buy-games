def exclude_copies(queryset):
    last_pk = queryset.last().pk
    index = 1
    products_to_exclude = []
    while index <= last_pk:
        products = queryset.filter(pk=index)
        try:

            if products.exists():
                product = products.first()
                adi_copies = product.similar_products()
                copies_pk = [i.product.pk for i in adi_copies][1:]
                products_to_exclude.extend(copies_pk)
        except:
            print(products.first().similar_products())

        index += 1
    return queryset.exclude(pk__in=products_to_exclude)
