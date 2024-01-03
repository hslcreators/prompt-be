from .models import Review


def calculate_average_rating(review: Review):
    printer = review.printer

    add = 0
    for one_review in Review.objects.filter(printer=printer):
        if one_review.id == review.id:
            add += review.rating
        else:
            add += one_review.rating

    average = add / len(Review.objects.filter(printer=printer))

    printer.average_rating = round(average)
    printer.save()
