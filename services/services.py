def create_products_list_for_bag(bag_products: list[tuple]):
    final_list = ''
    shablon = '{} - {} шт. x {} руб. = {} руб.\n'
    for product in bag_products:
        final_list += shablon.format(product[4], product[2], product[3], product[3]*product[2])
    return final_list

def count_itogo(bag_products: list[tuple]):
    itogo = 0
    for product in bag_products:
        itogo += product[3]*product[2]
    return itogo
