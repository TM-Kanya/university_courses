
'''
Credit Card Simulator
Authors: Michael Guerzhoy (starter code) and Tanvi Manku (completed functions)
'''

def initialize():
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global card_disabled
    global MONTHLY_INTEREST_RATE

    # Represents whether card has been disabled due to purchases in 3 different countries in a row. False if card is still active, True if it has been deactivated.
    card_disabled = False

    # Amount currently accruing interest.
    cur_balance_owing_intst = 0

    # Amount currently not accruing interest.
    cur_balance_owing_recent = 0

    # Records the last date (day, month) an operation was performed.

    last_update_day, last_update_month = 0, 0

    # Records the last two countries in which purchases were made.
    last_country = None
    last_country2 = None

    # The interest rate of the amount accumulating interest.
    MONTHLY_INTEREST_RATE = 1.05


def date_same_or_later(day1, month1, day2, month2):
    """
    Purpose:
    - Check if date at day1, month1 is the same or after the date at day2, month2.

    Parameters:
    - day1 -- day of date being checked to be the same or later.
    - month1 -- month of date being checked to be the same or later.
    - day2 -- day of date used to compare the date represented by day1, month1.
    - month2 -- month of date used to compare the date represented by day1, month1.

    Returns:
    - Boolean.
    - True if day1, month1 is the same or after day2, month2, otherwise returns False.

    Assumes:
    - day1, month1, day2, and month2 are valid dates in the year 2020.
    """

    if month1 > month2 or (month1 == month2 and day1 >= day2):
        return True

    return False


def all_three_different(c1, c2, c3):
    """
    Purpose:
    - Check if the values of c1, c2, and c3 are unique and different.

    Parameters:
    - c1 -- one of the three strings to be compared.
    - c2 -- one of the three strings to be compared.
    - c3 -- one of the three strings to be compared.

    Returns:
    - Boolean.
    - True if c1, c2, and c3 are all different values, otherwise returns False.

    Assumes:
    - c1, c2, and c3 are all strings.
    """

    if c1 != c2 and c1 != c3 and c2 != c3:
        return True

    return False


def purchase(amount, day, month, country):
    """
    Purpose:
    - Simulate a purchase using the credit card

    Parameters:
    - amount -- amount of purchase.
    - day -- day of purchase.
    - month -- month of purchase.
    - country -- country where purchase was made.

    Returns:
    - string "error" if:
      - the credit card is or will be disabled due to purchases in 3 different countries in a row, or
      - there was already an operation performed on a date later than day, month.
    - otherwise, None.

    Assumes:
    - amount is not a negative number (is greater than 0).
    - day, month is a valid date in the year 2020.
    - country is a valid country name.
    """

    global cur_balance_owing_intst, cur_balance_owing_recent, last_update_day, last_update_month, last_country, last_country2, card_disabled

    if card_disabled == True or (last_country2 != None and all_three_different(last_country, last_country2, country) == True):
        card_disabled = True
        return "error"
    elif date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return "error"

    months_passed = month - last_update_month

    if months_passed == 0:
        cur_balance_owing_recent += amount
    else:
        # Calculate amount owing interest of as of day, month
        for i in range(months_passed):
            cur_balance_owing_intst = cur_balance_owing_intst * MONTHLY_INTEREST_RATE
            cur_balance_owing_intst += cur_balance_owing_recent
            cur_balance_owing_recent = 0

        cur_balance_owing_recent = amount

    last_update_day = day
    last_update_month = month

    last_country2 = last_country
    last_country = country


def amount_owed(day, month):
    """
    Purpose:
    - Check the amount owed as of the date at day, month.

    Parameters:
    - day -- day of date the amount owed is being checked.
    - month -- month of date the amount owed is being checked.

    Returns:
    - string "error" if there was already an operation performed on a date later than day, month.
    - otherwise, number representing the total amount owed (amount accumuluting interest plus the amount not accumuluting interest).

    Assumes:
    - day, month is a valid date in the year 2020.
    """

    global cur_balance_owing_intst, cur_balance_owing_recent, last_update_day, last_update_month

    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return "error"

    months_passed = month - last_update_month

    # Calculate amount owing interest of as of day, month
    if months_passed > 0 :
        for i in range(months_passed):
            cur_balance_owing_intst = cur_balance_owing_intst * MONTHLY_INTEREST_RATE
            cur_balance_owing_intst += cur_balance_owing_recent
            cur_balance_owing_recent = 0

    last_update_day = day
    last_update_month = month

    return cur_balance_owing_recent + cur_balance_owing_intst

def pay_bill(amount, day, month):
    """
    Purpose:
    - Simulate a payment of the amount owed on the credit card

    Parameters:
    - amount -- amount of payment.
    - day -- day of payment.
    - month -- month of payment.

    Returns:
    - string "error" there was already an operation performed on a date later than day, month.
    - otherwise, None.

    Assumes:
    - amount is not a negative number (is greater than 0).
    - day, month is a valid date in the year 2020.
    """

    global cur_balance_owing_intst, cur_balance_owing_recent, last_update_day, last_update_month

    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return "error"

    months_passed = month - last_update_month

    # Calculate amount owing interest of as of day, month
    if months_passed > 0 :
        for i in range(months_passed):
            cur_balance_owing_intst = cur_balance_owing_intst * MONTHLY_INTEREST_RATE
            cur_balance_owing_intst += cur_balance_owing_recent
            cur_balance_owing_recent = 0

        if months_passed >= 1:
            cur_balance_owing_recent = 0

    last_update_day = day
    last_update_month = month

    # Checking the amount being paid and changing values of amount owed accordingly
    if amount == (cur_balance_owing_intst + cur_balance_owing_recent):
        cur_balance_owing_intst = 0
        cur_balance_owing_recent = 0

    elif amount < cur_balance_owing_intst:
        cur_balance_owing_intst = cur_balance_owing_intst - amount

    elif amount > cur_balance_owing_intst and (amount - cur_balance_owing_intst) < cur_balance_owing_recent:
        cur_balance_owing_recent = cur_balance_owing_recent - (amount - cur_balance_owing_intst)
        cur_balance_owing_intst = 0

# Initialize all global variables outside the main block.
initialize()

if __name__ == '__main__':
    # Testing date_same_or_later
    print("Testing date_same_or_later")
    print(date_same_or_later(1, 6, 12, 2)) # month1 > month2, day1 < day2; True
    print(date_same_or_later(1, 2, 12, 2)) # month1 = month2, day1 < day2; False
    print(date_same_or_later(1, 2, 1, 2)) # month1 = month2, day1 = day2; True
    print(date_same_or_later(10, 8, 5, 6)) # month1 > month2, day1 > day2; True
    print(date_same_or_later(20, 1, 5, 2)) # month1 < month2, day1 > day2; False
    print(date_same_or_later(5, 8, 5, 6)) # month1 > month2, day1 = day2; True
    print(date_same_or_later(5, 4, 5, 6)) # month1 < month2, day1 = day2; False
    print("-"*25)

    # Testing all_three_different
    print("Testing all_three_different")
    print(all_three_different("Canada", "Peru", "India")) # all three different; True
    print(all_three_different("Canada", "Canada", "India")) # two are same, one is different; False
    print(all_three_different("India", "India", "India")) # all three are same; False
    print("-"*25)

    # Testing from "Project #1 - General Instructions"
    initialize()
    purchase(80, 8, 1, "Canada")
    print("Now owing:", amount_owed(8, 1))      # 80.0
    pay_bill(50, 2, 2)
    print("Now owing:", amount_owed(2, 2))      # 30.0     (=80-50)
    print("Now owing:", amount_owed(6, 3))      # 31.5     (=30*1.05)
    purchase(40, 6, 3, "Canada")
    print("Now owing:", amount_owed(6, 3))      # 71.5     (=31.5+40)
    pay_bill(30, 7, 3)
    print("Now owing:", amount_owed(7, 3))      # 41.5     (=71.5-30)
    print("Now owing:", amount_owed(1, 5))      # 43.65375 (=1.5*1.05*1.05+40*1.05)
    purchase(40, 2, 5, "France")
    print("Now owing:", amount_owed(2, 5))      # 83.65375
    print(purchase(50, 3, 5, "United States"))  # error    (3 diff. countries in
                                                #          a row)

    print("Now owing:", amount_owed(3, 5))      # 83.65375 (no change, purchase
                                                #           declined)
    print(purchase(150, 3, 5, "Canada"))        # error    (card disabled)
    print("Now owing:", amount_owed(1, 6))      # 85.8364375
                                                # (43.65375*1.05+40)
    print("-"*25)

    # Testing multiple cases
    initialize()
    print("Now owing:", amount_owed(1, 1))      # 0.0
    purchase(10, 31, 1, "Canada")
    print("Now owing:", amount_owed(31, 1))     # 10.0
    print("Now owing:", amount_owed(1, 2))      # 10.0
    purchase(10, 1, 3, "India")
    print("Now owing:", amount_owed(1, 3))      # 20.5    (= 10 + 10 * 1.05)
    print("Now owing:", amount_owed(31, 3))     # 20.5
    purchase(15, 16, 4, "Canada")               # 36.025  (= 15 + 10 + 10 * 1.05 ^ 2)
    print("Now owing:", amount_owed(12, 5))     # 37.07625(= 15 + 10 * 1.05 + 10 * 1.05 ^ 3)
    pay_bill(17.07625, 12, 5)
    print("Now owing:", amount_owed(12, 5))     # 20.0     (= 37.07625 - 17.07625)
    print("Now owing:", amount_owed(25, 8))     # 23.15255 (= 20 * 1.05^3)
    purchase(7, 31, 8, "India")
    print("Now owing:", amount_owed(31, 8))     # 30.15255  (= 23.15255 + 7)
    print("Now owing:", amount_owed(5, 9))      # 31.31 (= 23.15 * 1.05 + 7)

    print(purchase(7, 20, 2, "Peru"))           # error (not a valid date)
    print("Now owing:", amount_owed(20, 2))     # error (not a valid date)

    print("Now owing:", amount_owed(5, 12))     # 36.245 (= 31.31 * 1.05 ^ 3)

    print(purchase(7, 28, 12, "Greece"))        # error (disabled)

    print(purchase(7, 31, 12, "Greece"))        # error (disabled)

    # Additional tests were performed using shared testing code from Andy Gong, Abdul Asad, and Nathan Chin
