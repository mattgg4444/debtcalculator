#Debt calculator program

import csv
import matplotlib.pyplot as plt

def plot_debt_over_time(table):
    months = [row[0] for row in table]
    remaining_debt = [row[3] for row in table]
    plt.plot(months, remaining_debt)
    plt.title("Debt Over Time")
    plt.xlabel("Month")
    plt.ylabel("Remaining Debt (€)")
    plt.grid(True)
    plt.show()

"""

This here doesnt work for now, I want to add it later.

def paid_interest_over_time(table):
    months = [row[0] for row in table]
    interest_paid = sum(row[1] for row in table)
    plt.plot(months, interest_paid)
    plt.title("Debt Over Time")
    plt.xlabel("Month")
    plt.ylabel("Total Interest Paid (€)")
    plt.grid(True)
    plt.show() """


def get_valid_input(prompt):
    while True:
        value = input(prompt).strip().upper()
        if value not in ["Y", "M"]:
            print("Please enter 'M' for months or 'Y' for years.")
            continue
        return value


def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
                continue
            return value  # If all is good, return the value
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_user_decision(): # get the decision on whether to calculate the rate OR time in months
    """
        Ask the user whether to calculate the monthly rate or the time.
        Returns:
            0 if user wants to calculate rate,
            1 if user wants to calculate time,
           -1 if user quits.
        """
    while True:
        print("Calculate rate based on total time of the credit, or"
              " calculate time to pay back the credit with a chosen rate?")
        user_decision = input("Press 'C' to calculate a monthly rate, 'E' to enter a rate and"
                              " calculate the remaining time: Press 'Q' to quit the program. ").strip().upper()
        if user_decision == "C":
            return 0
        elif user_decision == "E":
            return 1
        elif user_decision == "Q":  # Allow quitting
            return -1
        else:
            print("Press 'C', 'E', or 'Q' to quit: ")
            continue


def calculate_monthly_rate(time, int_rate, initial_debt): # calculates the monthly rate to pay off the debt
    if time < 1:
        raise ValueError("Time must be at least 1 month.")
    monthly_int = int_rate / 100 / 12  # Monthly interest rate
    months = round(time)  # Ensure integer for months
    if monthly_int == 0:  # Handle zero interest rate
        return initial_debt / months
    return initial_debt * monthly_int / (1 - (1 + monthly_int) ** -months)


def get_user_rate(minimal_rate):
    while True:
        try:
            monthly_rate = float(input("Enter rate: "))
            if monthly_rate <= 0 or monthly_rate <= minimal_rate:
                print(f"Value cannot be negative or smaller than minimum rate: {minimal_rate:.2f}.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        return monthly_rate


def calc_minimum_rate(initial_debt, int_rate):
    minimal_rate = (initial_debt * int_rate / 100 / 12)
    print(f"Minimum rate: {minimal_rate:.2f}")
    return minimal_rate

def time_calc(monthly_rate, int_rate, initial_debt):
    print(f"Calculating time in months to pay off the debt with desired monthly rate: {monthly_rate}")
    months_needed  = 0
    while initial_debt > 0:
        monthly_int = (initial_debt * int_rate / 100 / 12)
        clearance = monthly_rate - monthly_int
        initial_debt -= clearance
        months_needed  += 1
    return months_needed


def time_variable(time_unit):
    while True:
        try:
            time = float(input(f"Enter time in {'years' if time_unit == 'Y' else 'months'}: "))
            if time < 0:
                print("Time cannot be negative.")
                continue
            if time_unit == "Y":
                time = time * 12  # Convert years to months
                return time  # Exit the inner loop after valid input
            elif time_unit == "M":
                return time

        except ValueError:
            print("Invalid input. Please enter a whole number.")

def user_decision_amortization(): # Returns 0 if no amortization table, 1 if yes
    while True:
        amortization = input("Press 'Y' to show amortization table, or 'N' to not: ").strip().upper()
        if amortization == "N":
            return 0
        elif amortization not in ["Y", "N"]:
            print("Please enter 'Y' or 'N'.")
            continue
        else:
            return 1

def amortization_table(monthly_rate, time, int_rate, initial_debt):
            time = round(time)
            print("*********************")
            print("Calculating table...")
            print("*********************")
            table = []
            for months in range(1, time + 1):
                monthly_int = (initial_debt * int_rate / 100 / 12)
                clearance = monthly_rate - monthly_int
                initial_debt = initial_debt - clearance
                if initial_debt < 0: initial_debt = 0
                table.append([months, monthly_int, monthly_rate, initial_debt])
                print(f" Month {months:5}: Monthly interest: {monthly_int:7.2f} Total payment: {monthly_rate:7.2f} Remaining debt: {initial_debt:7.2f}")
            return table

def total_interest_paid(table):
    return sum(row[1] for row in table)  # row[1] is interest column


def export_amortization_table_to_csv(table, filename="debt_amortization.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Month", "Interest", "Payment", "Remaining Debt"])
        for row in table:
            writer.writerow(row)

def print_summary(initial_debt, int_rate, time, monthly_rate):
    print(f"Initial debt: {initial_debt:.0f}")
    print(f"Interest Rate in %: {int_rate:.2f}")
    print(f"Rest time of credit in months: {time:.0f}")
    print(f"Monthly payment (principal + interest): {monthly_rate:.2f}")


def handle_amortization_flow(monthly_rate, time, int_rate, initial_debt):
    amort_decision = user_decision_amortization()
    if amort_decision == 0:
        print("Goodbye.")
        return
    elif amort_decision == 1:
        table = amortization_table(monthly_rate, time, int_rate, initial_debt)
        export_amortization_table_to_csv(table, filename="debt_amortization.csv")
        total_interest = total_interest_paid(table)
        print("*********************")
        print(f"Total interest paid: {total_interest:.2f}")
        print("*********************")
        print("Amortization table saved as .csv!")
        plot_debt_over_time(table)


def calculate_by_time(int_rate, initial_debt):
    time_unit = get_valid_input("Enter time in years or months: 'Y' for Years, 'M' for Months: ")
    time = time_variable(time_unit)
    monthly_rate = calculate_monthly_rate(time, int_rate, initial_debt)
    print_summary(initial_debt, int_rate, time, monthly_rate)
    handle_amortization_flow(monthly_rate, time, int_rate, initial_debt)


def calculate_by_rate(int_rate, initial_debt):
    minimal_rate = calc_minimum_rate(initial_debt, int_rate)
    monthly_rate = get_user_rate(minimal_rate)
    time = time_calc(monthly_rate, int_rate, initial_debt)
    print_summary(initial_debt, int_rate, time, monthly_rate)
    handle_amortization_flow(monthly_rate, time, int_rate, initial_debt)


def main():
    initial_debt = get_positive_float("Enter amount of the debt: ")
    int_rate = get_positive_float("Enter interest rate in %, e.g. '4.3': ")
    decision = get_user_decision()

    if decision == -1:
        print("Goodbye.")
        return

    elif decision == 0:
        calculate_by_time(int_rate, initial_debt)

    elif decision == 1:
        calculate_by_rate(int_rate, initial_debt)

# if __name__ == "__main__":
#     main()
