from apps.authentication.models import Printer
from apps.orders.models import Order


def order_charge(printer: Printer, no_of_copies: int, pages: int, coloured: bool):

    if coloured:
        return no_of_copies * pages * printer.coloured_rate
    else:
        return no_of_copies * pages * printer.uncoloured_rate
