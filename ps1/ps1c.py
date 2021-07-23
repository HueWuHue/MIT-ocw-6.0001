# Asking for inputs
annual_salary = float(input("Enter the starting salary: "))
# Initializing the variables
og_salary = annual_salary # Placeholder to retrieve original salary
total_cost = 1000000
semi_annual_raise = .07
portion_down_payment = 0.25*total_cost
current_savings = 0
r = 0.04
epilson = 100
low = 0
high = 10000
bisect_count = 0
bisect = 10000
# Conditional loop
while current_savings < (portion_down_payment - epilson) or current_savings > (portion_down_payment + epilson):
    # For loop over 36 months
    for months in range(36):
        current_savings += current_savings*(r/12)
        current_savings += (annual_salary/12)*(bisect/10000)
        if (months+1) % 6 == 0:
            annual_salary *= (1+semi_annual_raise)
    # Check if it is possible to pay the down payment - 1

    # Display this message if unable to pay down payment - 1
    if bisect == 10000 and current_savings < (portion_down_payment-epilson):
        print("It is not possible to pay the down payment in three years.")
        break
    else:
        # Decreases the bisect value range if savings got too high
        if current_savings > (portion_down_payment + epilson):
            high = bisect
        # Increases the bisect value range if savings were not enough
        elif current_savings < (portion_down_payment - epilson):
            low = bisect
        # Jackpot (Ding!Ding!)
        else:
            bisect_count += 1
            print("Best savings rate: ",bisect/10000)
            print("Steps in bisection search",bisect_count)
            break
        # Resetting variables
        bisect = (high+low)/2
        current_savings = 0
        annual_salary = og_salary
        bisect_count += 1
