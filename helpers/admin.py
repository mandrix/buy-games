def exclude_copies(queryset):
    last_pk = queryset.last().pk
    index = 1
    products_to_exclude = []
    while index <= last_pk:
        products = queryset.filter(pk=index)
        if products.exists():
            product = products.first()
            adi_copies = product.similar_products()
            if adi_copies:
                copies_pk = [i.product.pk for i in adi_copies if not isinstance(i, str)][1:]
                products_to_exclude.extend(copies_pk)

        index += 1
    return queryset.exclude(pk__in=products_to_exclude)
