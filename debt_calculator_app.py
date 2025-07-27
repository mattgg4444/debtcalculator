import tkinter as tk
from tkinter import messagebox

from DebtCalculator import calculate_monthly_rate, time_calc, total_interest_paid, amortization_table


# Create the main window
def main():
    root = tk.Tk()
    root.title("Debt Calculator")
    root.geometry("500x500")

    # === Mode Switch ===
    mode_var = tk.StringVar(value="Monthly Payment")

    def update_fields(*args):
        mode = mode_var.get()
        if mode == "Monthly Payment":
            entry_time.configure(state="normal")
            entry_monthly.configure(state="disabled")
        else:
            entry_time.configure(state="disabled")
            entry_monthly.configure(state="normal")

    tk.Label(root, text="Select Calculation Mode:").pack(pady=(10, 0))
    mode_menu = tk.OptionMenu(root, mode_var,
                              "Monthly Payment", "Repayment Time")
    mode_menu.pack()
    mode_var.trace_add("write", update_fields)

    # Labels and entries # GUI layout
    tk.Label(root, text="Initial Debt (€):").pack()
    entry_debt = tk.Entry(root)
    entry_debt.pack()

    tk.Label(root, text="Interest Rate (%):").pack()
    entry_rate = tk.Entry(root)
    entry_rate.pack()

    tk.Label(root, text="Monthly Payment (€):").pack()
    entry_monthly = tk.Entry(root)
    entry_monthly.pack()
    entry_monthly.configure(state="disabled")  # Only enabled in repayment_time mode

    tk.Label(root, text="Time (months):").pack()
    entry_time = tk.Entry(root)
    entry_time.pack()


    def get_validated_inputs():
        # Get and validate inputs
        debt_str = entry_debt.get().strip()
        rate_str = entry_rate.get().strip()
        if not debt_str:
            raise ValueError("Initial Debt cannot be empty")
        if not rate_str:
            raise ValueError("Interest Rate cannot be empty")
        debt = float(debt_str)
        rate = float(rate_str)
        if debt <= 0:
            raise ValueError("Initial Debt must be positive")
        if rate < 0:
            raise ValueError("Interest Rate cannot be negative")

        mode = mode_var.get()
        if mode == "Monthly Payment":
            time_str = entry_time.get().strip()
            if not time_str:
                raise ValueError("Time cannot be empty")
            time = float(time_str)
            if time <= 0:
                raise ValueError("Time must be positive")
            monthly = calculate_monthly_rate(time, rate, debt)
        else:
            minimal_rate = (debt * rate / 100 / 12)
            monthly_str = entry_monthly.get().strip()
            if not monthly_str:
                raise ValueError("Monthly Payment cannot be empty")
            monthly = float(monthly_str)
            if monthly <= 0:
                raise ValueError("Monthly Payment must be positive")
            elif monthly <= minimal_rate:
                raise ValueError(f"Monthly Payment must be greater than Interest rate {minimal_rate:.2f}")
            time = time_calc(monthly, rate, debt)
        return debt, rate, monthly, time


    def calculate():
        try:
            debt, rate, monthly, time = get_validated_inputs()
            mode = mode_var.get()
            if mode == "Monthly Payment":
                result_label.config(text=f"Monthly Payment: €{monthly:.2f}")
            else:
                result_label.config(text=f"Months Needed: {round(time)}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def calculate_total_int():
        try:
            debt, rate, monthly, time = get_validated_inputs()
            #Get amortization table and calculate total interest
            table = amortization_table(monthly, time, rate, debt)
            total_interest = total_interest_paid(table)
            total_interest_paid_label.config(text=f"Total Interest Paid: €{total_interest:.2f}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def reset_buttons():
        # Clear all Entry widgets
        entry_debt.delete(0, tk.END)
        entry_rate.delete(0, tk.END)
        entry_monthly.delete(0, tk.END)
        entry_time.delete(0, tk.END)

        # Reset labels to empty text
        result_label.config(text="")
        total_interest_paid_label.config(text="")

    def exit_program():
        root.destroy()


    tk.Button(root, text="Calculate", command=calculate).pack(pady=10)
    result_label = tk.Label(root, text="", fg="blue")
    result_label.pack(pady=10)
    tk.Button(root, text="Show Total Interest Paid", command=calculate_total_int).pack(pady=10)
    total_interest_paid_label = tk.Label(root, text="", fg="orange")
    total_interest_paid_label.pack(pady=10)
    tk.Button(root, text="Reset Input", command=reset_buttons).pack(pady=10)
    tk.Button(root, text="Exit Program", command=exit_program).pack(pady=10)

    # Run the app
    root.mainloop()


if __name__ == "__main__":
    main()