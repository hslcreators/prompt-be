from .models import Review


def calculate_average_rating(review: Review):
    printer = review.printer

    add = 0
    for one_review in Review.objects.filter(printer=printer):
        if one_review.id == review.id:
            add += int(review.rating)
        else:
            add += int(one_review.rating)

    if len(Review.objects.filter(printer=printer)) == 0:
        average = 0
    else:
        average = add / len(Review.objects.filter(printer=printer))

    printer.average_rating = round(average)
    printer.save()
