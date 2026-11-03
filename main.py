from datetime import date
from mysql import connector


class CarShowroomManager:
    def get_connection(self):
        try:
            self.connection = connector.connect(
                host="localhost",
                user="root",
                password="YOUR_PASSWORD",
                database="car_showroom_db"
            )
            return self.connection
        except Exception as e:
            print(e)
            return None


    def add_car(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            brand = input("Enter brand: ")
            model = input("Enter model: ")
            year = int(input("Enter year: "))
            color = input("Enter color: ")
            fuel_type = input("Enter fuel type (Petrol/Diesel/Electric): ")
            price = float(input("Enter price: "))
            stock = int(input("Enter stock: "))

            query = """
            INSERT INTO car (brand, model, year, color, fuel_type, price, stock)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (brand, model, year, color, fuel_type, price, stock))
            connection.commit()
            print("Car Added Successfully.")
            connection.close()
        except Exception as e:
            print(e)

    def get_cars(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM car")
            for car in cursor.fetchall():
                print(car)
            connection.close()
        except Exception as e:
            print(e)

    def search_car(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            keyword = input("Enter brand or model to search: ")
            query = "SELECT * FROM car WHERE brand LIKE %s OR model LIKE %s"
            like = f"%{keyword}%"
            cursor.execute(query, (like, like))
            records = cursor.fetchall()
            if not records:
                print("No cars found.")
            for car in records:
                print(car)
            connection.close()
        except Exception as e:
            print(e)

    def update_car(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            car_id = int(input("Enter car id: "))
            brand = input("Enter new brand: ")
            model = input("Enter new model: ")
            year = int(input("Enter new year: "))
            color = input("Enter new color: ")
            fuel_type = input("Enter new fuel type: ")
            price = float(input("Enter new price: "))
            stock = int(input("Enter new stock: "))

            query = """
            UPDATE car
            SET brand=%s, model=%s, year=%s, color=%s,
                fuel_type=%s, price=%s, stock=%s
            WHERE id=%s
            """
            cursor.execute(query, (brand, model, year, color, fuel_type, price, stock, car_id))
            connection.commit()
            print("Car Updated Successfully.")
            connection.close()
        except Exception as e:
            print(e)

    def delete_car(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            car_id = int(input("Enter car id: "))
            cursor.execute("DELETE FROM car WHERE id=%s", (car_id,))
            connection.commit()
            print("Car Deleted Successfully.")
            connection.close()
        except Exception as e:
            print(e)


    def add_customer(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            name = input("Enter name: ")
            place = input("Enter place: ")
            mobile = input("Enter mobile: ")
            email = input("Enter email: ")

            query = """
            INSERT INTO customer (name, place, mobile, email)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (name, place, mobile, email))
            connection.commit()
            print("Customer Added Successfully.")
            connection.close()
        except Exception as e:
            print(e)

    def get_customers(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM customer")
            for customer in cursor.fetchall():
                print(customer)
            connection.close()
        except Exception as e:
            print(e)


    def sell_car(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            car_id = int(input("Enter car id: "))
            customer_id = int(input("Enter customer id: "))

            cursor.execute("SELECT price, stock FROM car WHERE id=%s", (car_id,))
            row = cursor.fetchone()
            if row is None:
                print("Car not found.")
                connection.close()
                return
            price, stock = row
            if stock <= 0:
                print("Car out of stock.")
                connection.close()
                return

            cursor.execute("SELECT id FROM customer WHERE id=%s", (customer_id,))
            if cursor.fetchone() is None:
                print("Customer not found.")
                connection.close()
                return

            cursor.execute(
                "INSERT INTO sale (car_id, customer_id, sale_date, sale_price) "
                "VALUES (%s, %s, %s, %s)",
                (car_id, customer_id, date.today(), price)
            )
            cursor.execute("UPDATE car SET stock = stock - 1 WHERE id=%s", (car_id,))
            connection.commit()
            print(f"Car Sold Successfully for {price}.")
            connection.close()
        except Exception as e:
            print(e)

    def get_sales(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            query = """
            SELECT s.id, c.brand, c.model, cu.name, s.sale_date, s.sale_price
            FROM sale s
            JOIN car c ON s.car_id = c.id
            JOIN customer cu ON s.customer_id = cu.id
            ORDER BY s.sale_date DESC
            """
            cursor.execute(query)
            records = cursor.fetchall()
            if not records:
                print("No sales yet.")
            for row in records:
                print(row)
            connection.close()
        except Exception as e:
            print(e)

    def total_sales(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*), COALESCE(SUM(sale_price), 0) FROM sale")
            count, total = cursor.fetchone()
            print(f"Cars sold: {count}")
            print(f"Total revenue: {total}")
            connection.close()
        except Exception as e:
            print(e)


def main():
    showroom = CarShowroomManager()
    actions = {
        "1": showroom.add_car,
        "2": showroom.get_cars,
        "3": showroom.search_car,
        "4": showroom.update_car,
        "5": showroom.delete_car,
        "6": showroom.add_customer,
        "7": showroom.get_customers,
        "8": showroom.sell_car,
        "9": showroom.get_sales,
        "10": showroom.total_sales,
    }

    while True:
        print("\n===== CAR SHOWROOM MANAGEMENT =====")
        print("1. Add Car")
        print("2. View Cars")
        print("3. Search Car")
        print("4. Update Car")
        print("5. Delete Car")
        print("6. Add Customer")
        print("7. View Customers")
        print("8. Sell Car")
        print("9. View Sales")
        print("10. Total Sales Report")
        print("0. Exit")

        choice = input("Enter choice: ")
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()