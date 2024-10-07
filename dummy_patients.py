import mysql.connector
from mysql.connector import Error
from faker import Faker
import random

fake = Faker()

try:
    connection = mysql.connector.connect(
        host='localhost', 
        port=3307,         
        database='medical_labdb', 
        user='imap',  
        password='44@@44aa00@Allan' 
    )

    if connection.is_connected():
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO patients (phone_number, full_name, gender, dob, age, address, medical_history, test_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        def generate_dummy_data(num_records):
            data = []
            genders = ['Male', 'Female', 'Other']
            for _ in range(num_records):
                phone_number = fake.phone_number()[:15]  
                full_name = fake.name()
                gender = random.choice(genders)
                dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
                age = (2024 - dob.year)  
                address = fake.address().replace('\n', ', ')  
                medical_history = fake.text(max_nb_chars=200)
                test_id = random.randint(1, 100)  
                data.append((phone_number, full_name, gender, dob, age, address, medical_history, test_id))
            return data

        dummy_data = generate_dummy_data(100)

        cursor.executemany(insert_query, dummy_data)
        connection.commit()
        print(f"{cursor.rowcount} records inserted successfully")

except Error as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
