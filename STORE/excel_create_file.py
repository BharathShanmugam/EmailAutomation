import pandas as pd
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# Generate random data
def generate_data(num_records):
    data = []
    for _ in range(num_records):
        firstname = fake.first_name()
        lastname = fake.last_name()
        company = fake.company()
        email = fake.email() if random.choice([True, False]) else None
        role = fake.job() if random.choice([True, False]) else None
        
        data.append({
            'firstname': firstname,
            'lastname': lastname,
            'company': company,
            'email': email,
            'role': role
        })
    return data

if __name__ == "__main__":
    num_records = 10  # Specify the number of records you want
    records = generate_data(num_records)
    
    # Create a DataFrame
    df = pd.DataFrame(records)

    # Save to Excel
    df.to_excel('random_data.xlsx', index=False)
