








def percent(part, whole):
    try:
        return 100 * float(part) / float(whole)
    except ZeroDivisionError:
        return 0