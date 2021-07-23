# Asking for inputs
annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to be save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))
# Initializing the variables
portion_down_payment = 0.25*total_cost
current_savings = 0
r = 0.04
months = 0
# Conditional loop
while current_savings<portion_down_payment:
    current_savings += current_savings*(r/12)
    current_savings += (annual_salary/12)*portion_saved
    months += 1  # Counter
print("Number of months :",months)
