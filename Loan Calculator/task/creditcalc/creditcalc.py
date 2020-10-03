import math
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--type", help="indicates the type of payment", type=str)
parser.add_argument("--payment", help="monthly payment amount", type=float)
parser.add_argument("--principal", help="initial loan amount", type=int)
parser.add_argument("--periods", help="number of months to repay loan", type=int)
parser.add_argument("--interest", help="non-nominal interest", type=float)
arguments = parser.parse_args()


def check_args(args):
    pay_type, monthly_payment, principal, periods, interest = args.type, args.payment, args.principal, args.periods, args.interest
    int_parameters = [monthly_payment, principal, periods, interest]
    all_parameters = [pay_type, monthly_payment, principal, periods, interest]
    entered_parameters = 2
    for num in int_parameters:
        if num is None:
            entered_parameters -= 1
            if entered_parameters == 0:
                print("Incorrect parameters")
                return False
        elif num < 0:
            print("Incorrect parameters")
            return False
    if not pay_type or not interest or pay_type != "annuity" and pay_type != "diff":
        print("Incorrect parameters")
        return False
    elif pay_type == "diff" and monthly_payment:
        print("Incorrect parameters")
        return False
    else:
        return all_parameters


def annuity_time(principal, monthly, interest):
    months = math.ceil(math.log(monthly / (monthly - (interest * principal)), 1 + interest))
    overpayment = int((monthly * months) - principal)
    years = months // 12
    months = months % 12
    if months != 0:
        print(f"It will take {years} years and {months} months to repay this loan!")
        print(f"Overpayment = {overpayment}")
    else:
        print(f"It will take {years} years to repay this loan!")
        print(f"Overpayment = {overpayment}")


def annuity_payments(principal, periods, interest):
    annuity = math.ceil(principal * ((interest * ((1 + interest) ** periods)) / ((1 + interest) ** periods - 1)))
    overpayment = (annuity * periods) - principal
    print(f"Your monthly payment = {annuity}!")
    print(f"Overpayment = {overpayment}")


def annuity_principal(annuity, periods, interest):
    interest_calc = (1 + interest) ** periods
    divisor = (interest * interest_calc) / (interest_calc - 1)
    principal = math.floor(annuity / divisor)
    print(f"Your loan principal = {principal}!")


def diff_payments(principal, periods, interest):
    calc_1 = principal / periods
    total_payment = 0
    for month in range(1, periods + 1):
        payment = math.ceil(calc_1 + interest * (principal - (principal * (month - 1) / periods)))
        total_payment += payment
        print(f"Month {month}: payment is {payment}")
    overpayment = total_payment - principal
    print(f"\nOverpayment = {overpayment}")


def main():
    if check_args(arguments):
        pay_type = check_args(arguments)[0]
        monthly_payment = check_args(arguments)[1]
        principal = check_args(arguments)[2]
        periods = check_args(arguments)[3]
        nominal_interest = check_args(arguments)[4] / 1200
        if pay_type == "annuity":
            if monthly_payment is None:
                annuity_payments(principal, periods, nominal_interest)
            elif periods is None:
                annuity_time(principal, monthly_payment, nominal_interest)
            else:
                annuity_principal(monthly_payment, periods, nominal_interest)
        else:
            diff_payments(principal, periods, nominal_interest)
    else:
        sys.exit()


main()
