

def calculate_grades(grades):

    if not grades:
        return "No grades available to calculate."

    if grades >= 90:
        return "A"
    elif grades >= 80:
        return "B"
    elif grades >= 70:
        return "C"
    elif grades >= 60:
        return "D"
    else:
        return "F"