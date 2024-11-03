import csv

def get_expenses(category_name, currency_symbol):
    expenses_input = input(f"Category: {category_name}\nPlease input expenses for the past 6 months in {currency_symbol}: ")
    expenses = [float(amount.strip()) for amount in expenses_input.split(',')]
    return expenses

def calculate_average(expenses):
    return sum(expenses) / len(expenses)

def calculate_savings_reduction(current_expense, reduction_percent):
    return current_expense * (reduction_percent / 100)

def main():
    categories = [
        ("Coffees", "MVR"),
        ("Dates", "MVR"),
        ("Dinner out", "MVR"),
        ("Entertainment", "MVR"),
        ("Uni Fee", "MVR"),
        ("Phone bill", "MVR")
    ]

    with open('expenses.csv', mode='w', newline='') as expenses_file:
        fieldnames = ["User Name", "Description", "Category", "Amount", "Date"]
        expenses_writer = csv.DictWriter(expenses_file, fieldnames=fieldnames)
        expenses_writer.writeheader()
        
        expenses_data = {}
        user_name = input("Welcome to the Expense Prediction Software\n>> Please input your name: ")
        print(f"Hello, {user_name}! Let's predict your expenses for next month.")
        
        while True:
            print("»› Please select an option:")
            print("1. Input Past Six Months' Expenses")
            print("2. Enter Expense Data")
            print("3. Predict Next Month's Expenses")
            print("4. Savings Plan for Next Month")
            print("5. Exit")

            choice = input("»> Enter your choice: ")

            if choice == '1':
                # Initialize a dictionary to store expense data for each category
                expense_data = {}
                for category, currency in categories:
                    expense_data[category] = get_expenses(category, currency)

                # Calculate and print the average expenses for each category
                print("\nAverage Expenses for Each Category:")
                for category, expenses in expense_data.items():
                    average_expense = calculate_average(expenses)
                    print(f"{category}: {average_expense:.2f} MVR")

                expenses_data.update(expense_data)

            elif choice == '2':
                print("»› You've selected 'Enter Expense Data'")
                description = input("Description of Expense: ")
                print("Category Options:")
                for index, (category, _) in enumerate(categories, start=1):
                    print(f"{index}. {category}")
                category_choice = int(input("Choose a Category: ")) - 1
                category, currency = categories[category_choice]
                amount = float(input(f"Amount in {currency}: "))
                date = input("Date (dd/mm/yyyy): ")
                print(">> Data Saved Successfully!")

                # Write the entered data to the CSV file
                expenses_writer.writerow({
                    "User Name": user_name,
                    "Description": description,
                    "Category": category,
                    "Amount": amount,
                    "Date": date
                })

                if category not in expenses_data:
                    expenses_data[category] = []

                expenses_data[category].append(amount)
            
            #3)prediction for the next month expenses and 4)savings plan for the next month will not take any input from 1)past six month data 
            #it's only takes data from the 2)enter expenses,in that aslo we have to give minimum three expenses for the each of the following(Coffees,Dates,Dinner out,Entertainment,Uni Fee,Phone bill)

            elif choice == '3':
                print("»› You've selected 'Predict Next Month's Expenses'")
                print("Calculating predictions based on past three months..")
                print("Predictions:")

                for category, expenses in expenses_data.items():
                    if len(expenses) >= 3:
                        past_three_months = expenses[-3:]
                        average_three_months = calculate_average(past_three_months)
                        predicted_expense = average_three_months
                        print(f"{category}: MVR {predicted_expense:.2f}")
                    else:
                        print(f"{category}: Not enough data for prediction")

            elif choice == '4':
                print("»› You've selected 'Savings Plan for Next Month'")
                savings_goal = float(input("Please enter your savings goal for next month: "))
                print("Recommendations:")
                category_currency = None

                for category, expenses in expenses_data.items():
                    if category in ["Coffees", "Dates", "Dinner out"]:
                        if len(expenses) >= 1:
                            current_expense = expenses[-1]
                            category_currency = next((currency for cat, currency in categories if cat == category), None)
                            if category_currency:
                                potential_savings = calculate_savings_reduction(current_expense, 10)
                                print(f"Consider reducing your {category.lower()} expense by 10%")
                                print(f"Potential Savings: MVR {potential_savings:.2f}")
                            else:
                                print(f"Category {category} not found in the list of categories.")

                if category_currency:
                    print(f"Adjust your savings goal or follow the recommendations to achieve your desired savings of MVR {savings_goal:.2f}")
                else:
                    print("No eligible categories found for recommendations.")

            elif choice == '5':
                print("Thank you for using the Expense Prediction & Savings Planner Software. Goodbye!")
                break

if __name__ == "__main__":
    main()

