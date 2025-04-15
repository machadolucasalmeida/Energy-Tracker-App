import csv

# ENERGY SPENT TRACKER APPLICATION
# --------------------------------
# This application tracks appliance energy consumption and cost.
# The code is separated into three main sections:
# 1. HELPER FUNCTIONS FOR INPUT VALIDATION
# 2. BUSINESS LOGIC & DATA PERSISTENCE FUNCTIONS
# 3. USER INTERFACE FUNCTIONS (including improved input validation and error handling)


# ===========================
# HELPER FUNCTIONS FOR INPUT VALIDATION
# ===========================
def get_positive_float(prompt):
    """
    Prompt the user until a valid positive float is entered.
    
    Parameters:
    - prompt (str): The prompt message to display.
    
    Returns:
    - float: A validated positive float value.
    """
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            else:
                print("❌ Please enter a positive number.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")


def get_int(prompt, min_value=None, max_value=None):
    """
    Prompt the user until a valid integer is entered.
    
    Parameters:
    - prompt (str): The prompt message to display.
    - min_value (int, optional): Minimum acceptable value.
    - max_value (int, optional): Maximum acceptable value.
    
    Returns:
    - int: A validated integer.
    """
    while True:
        try:
            value = int(input(prompt))
            if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                print("❌ Invalid selection. Please try again.")
            else:
                return value
        except ValueError:
            print("❌ Invalid input. Please enter a number.")


# ===========================
# BUSINESS LOGIC & DATA PERSISTENCE FUNCTIONS
# ===========================

def add_appliance(name, watts, hours_per_day):
    """
    Create and return a new appliance dictionary.

    Parameters:
    - name (str): The name of the appliance.
    - watts (float): The power consumption in watts.
    - hours_per_day (float): The number of hours the appliance is used per day.

    Returns:
    - dict: A dictionary containing the appliance details.
    """
    appliance = {
        "name": name,
        "watts": watts,
        "hours_per_day": hours_per_day
    }
    return appliance

def calculate_daily_kwh(watts, hours_per_day):
    """
    Calculate the daily energy consumption in kWh.

    Parameters:
    - watts (float): The power consumption in watts.
    - hours_per_day (float): The number of hours the appliance is used per day.

    Returns:
    - float: The daily energy consumption in kWh.
    """
    daily_kwh = (watts * hours_per_day) / 1000
    return daily_kwh

def calculate_monthly_kwh(daily_kwh):
    """
    Calculate monthly energy consumption in kWh based on daily usage.

    Parameters:
    - daily_kwh (float): The daily energy consumption in kWh.

    Returns:
    - float: The monthly energy consumption in kWh.
    """
    monthly_kwh = daily_kwh * 30
    return monthly_kwh

def calculate_cost(kwh, price_per_kwh):
    """
    Calculate the total cost based on energy consumption and unit price.

    Parameters:
    - kwh (float): The total energy consumption in kWh.
    - price_per_kwh (float): The price per kWh.

    Returns:
    - float: The total cost.
    """
    return kwh * price_per_kwh

# ----- DATA PERSISTENCE FUNCTIONS (CSV) -----

def save_appliances_to_csv(appliances, filename="appliances.csv"):
    """
    Save the list of appliances to a CSV file.

    Parameters:
    - appliances (list): A list of appliance dictionaries.
    - filename (str): The filename to save the data.
    """
    with open(filename, mode="w", newline="") as csv_file:
        fieldnames = ["name", "watts", "hours_per_day"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for appliance in appliances:
            writer.writerow(appliance)

def load_appliances_from_csv(filename="appliances.csv"):
    """
    Load the list of appliances from a CSV file.

    Parameters:
    - filename (str): The filename to load the data from.

    Returns:
    - list: A list of appliance dictionaries.
    """
    appliances = []
    try:
        with open(filename, mode="r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # Convert numeric fields from strings to float
                row["watts"] = float(row["watts"])
                row["hours_per_day"] = float(row["hours_per_day"])
                appliances.append(row)
    except FileNotFoundError:
        # If the file does not exist, return an empty list
        pass
    return appliances


# ===========================
# USER INTERFACE FUNCTIONS
# ===========================

def show_menu():
    """
    Display the main menu and return the user's chosen option.

    Returns:
    - str: The user's input corresponding to the menu option.
    """
    print("\n===== 🔌 ENERGY SPENT TRACKER =====")
    print("1. Add an appliance")
    print("2. Calculate usage and cost of a single appliance")
    print("3. Calculate total usage and cost of all appliances")
    print("4. Edit appliance list")
    print("5. View all appliances")
    print("0. Exit")
    return input("Choose an option: ")

def edit_appliance(appliances):
    """
    Allow the user to edit the attributes of an existing appliance or delete it.

    Parameters:
    - appliances (list): The list of appliance dictionaries.
    """
    if not appliances:
        print("⚠️ No appliances to edit.")
        return

    while True:
        print("\n🔧 Edit Appliances:")
        for i, app in enumerate(appliances):
            print(f"{i + 1}. {app['name']} | {app['watts']}W | {app['hours_per_day']}h/day")
        
        # Validate selection input
        choice = get_int("Select the appliance number to edit, or 0 to go back to the main menu: ", 0)
        choice -= 1  # Adjusting to 0-index
        
        if choice == -1:
            print("↩️ Returning to main menu.")
            return

        if 0 <= choice < len(appliances):
            app = appliances[choice]
            print(f"\nSelected appliance: {app['name']}")
            print("1. Edit name")
            print("2. Edit watts")
            print("3. Edit hours per day")
            print("4. Delete appliance")
            print("0. Go back to appliance list")

            sub_option = input("Choose an option: ").strip()

            if sub_option == '1':
                new_name = input(f"Enter new name (current: {app['name']}): ").strip()
                if new_name:
                    appliances[choice]['name'] = new_name
                    print("✅ Name updated successfully!")
                else:
                    print("❌ Name cannot be empty.")
            elif sub_option == '2':
                new_watts = get_positive_float(f"Enter new watts (current: {app['watts']}W): ")
                appliances[choice]['watts'] = new_watts
                print("✅ Watts updated successfully!")
            elif sub_option == '3':
                new_hours = get_positive_float(f"Enter new hours per day (current: {app['hours_per_day']}h): ")
                appliances[choice]['hours_per_day'] = new_hours
                print("✅ Hours updated successfully!")
            elif sub_option == '4':
                confirm = input(f"Are you sure you want to delete '{app['name']}'? (y/n): ").strip().lower()
                if confirm == 'y':
                    appliances.pop(choice)
                    print("🗑️ Appliance deleted successfully!")
                else:
                    print("❌ Deletion canceled.")
            elif sub_option == '0':
                print("↩️ Returning to appliance list.")
                continue
            else:
                print("❌ Invalid option.")
        else:
            print("❌ Invalid selection.")

def view_appliances(appliances):
    """
    Display a formatted list of all appliances.

    Parameters:
    - appliances (list): The list of appliance dictionaries.
    """
    if not appliances:
        print("⚠️ No appliances added yet.")
        return

    print("\n📋 Registered Appliances:")
    for i, app in enumerate(appliances):
        print(f"{i + 1}. {app['name']} || {app['watts']}W || {app['hours_per_day']}h/day")

def main():
    """
    The main entry point of the Energy Spent Tracker application.
    Handles the flow of user interaction.
    """
    # Load appliances from CSV file at startup
    appliances = load_appliances_from_csv()

    while True:
        option = show_menu().strip()

        if option == '1':
            # Adding a new appliance
            name = input("Enter appliance name: ").strip()
            if not name:
                print("❌ Appliance name cannot be empty.")
                continue

            watts = get_positive_float("Enter power (in watts): ")
            hours_per_day = get_positive_float("Enter hours used per day: ")
            appliances.append(add_appliance(name, watts, hours_per_day))
            print(f"✅ {name} added successfully!")

        elif option == '2':
            # Calculate and display usage and cost for a single appliance
            if not appliances:
                print("⚠️ No appliances added yet.")
                continue

            for i, app in enumerate(appliances):
                print(f"{i + 1}. {app['name']}")

            choice = get_int("Select appliance number: ", 1, len(appliances)) - 1

            price_per_kwh = get_positive_float("Enter price per kWh (e.g. 0.5): ")

            app = appliances[choice]
            daily = calculate_daily_kwh(app['watts'], app['hours_per_day'])
            monthly = calculate_monthly_kwh(daily)
            cost = calculate_cost(monthly, price_per_kwh)

            print(f"\n📊 {app['name']}")
            print(f"Daily usage: {daily:.2f} kWh")
            print(f"Monthly usage: {monthly:.2f} kWh")
            print(f"Estimated cost: ${cost:.2f}")

        elif option == '3':
            # Calculate and display total usage and cost for all appliances
            if not appliances:
                print("⚠️ No appliances added yet.")
                continue

            price_per_kwh = get_positive_float("Enter price per kWh (e.g. 0.5): ")

            total_monthly_kwh = 0
            total_cost = 0

            print("\n📊 INDIVIDUAL APPLIANCE USAGE:")
            for app in appliances:
                daily_kwh = calculate_daily_kwh(app['watts'], app['hours_per_day'])
                monthly_kwh = calculate_monthly_kwh(daily_kwh)
                monthly_hours = app['hours_per_day'] * 30
                cost = calculate_cost(monthly_kwh, price_per_kwh)

                total_monthly_kwh += monthly_kwh
                total_cost += cost

                print(f"🔹 {app['name']}")
                print(f"   ➤ Monthly kWh: {monthly_kwh:.2f} kWh")
                print(f"   ➤ Monthly hours used: {monthly_hours:.1f} h")
                print(f"   ➤ Estimated monthly cost: ${cost:.2f}\n")

            print("📈 TOTAL ENERGY USAGE & COST")
            print(f"   ➤ Total monthly usage: {total_monthly_kwh:.2f} kWh")
            print(f"   ➤ Total estimated cost: ${total_cost:.2f}")

        elif option == '4':
            # Edit existing appliance(s)
            edit_appliance(appliances)

        elif option == '5':
            # View all registered appliances
            view_appliances(appliances)

        elif option == '0':
            print("👋 Exiting the program. Goodbye!")
            break

        else:
            print("❌ Invalid option. Try again.")

    # Save appliances to CSV file on exit
    save_appliances_to_csv(appliances)
    print("Data saved to appliances.csv.")

if __name__ == "__main__":
    main()
