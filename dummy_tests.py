import mysql.connector
from mysql.connector import Error
from faker import Faker
import random

fake = Faker()

medical_diseases = {
    "Diabetes": "A chronic condition that affects the way the body processes blood sugar (glucose).",
    "Hypertension": "A condition in which the force of the blood against the artery walls is too high.",
    "Asthma": "A condition in which your airways narrow and swell and may produce extra mucus.",
    "Arthritis": "Inflammation of one or more joints, causing pain and stiffness that can worsen with age.",
    "Cancer": "A disease caused by an uncontrolled division of abnormal cells in a part of the body.",
    "Dementia": "A general term for a decline in mental ability severe enough to interfere with daily life.",
    "Heart Disease": "A range of conditions that affect your heart, such as coronary artery disease and arrhythmias.",
    "Hepatitis": "Inflammation of the liver, often caused by a viral infection.",
    "HIV/AIDS": "A virus that attacks the immune system, leading to life-threatening infections and cancers.",
    "Influenza": "A contagious respiratory illness caused by influenza viruses.",
    "Malaria": "A mosquito-borne infectious disease caused by parasites, resulting in fever, chills, and flu-like symptoms.",
    "Migraine": "A type of headache characterized by severe pain on one side of the head, often accompanied by nausea.",
    "Osteoporosis": "A condition in which bones become weak and brittle.",
    "Parkinson's Disease": "A neurodegenerative disorder that affects movement, causing tremors, stiffness, and slowness of movement.",
    "Pneumonia": "An infection that inflames the air sacs in one or both lungs, which may fill with fluid.",
    "Psoriasis": "A skin disease marked by red, itchy, scaly patches.",
    "Tuberculosis": "A potentially serious infectious disease that mainly affects the lungs.",
    "Ulcerative Colitis": "A chronic, inflammatory bowel disease that causes inflammation in the digestive tract.",
    "Alzheimer's Disease": "A progressive disease that destroys memory and other important mental functions.",
    "Lung Cancer": "A type of cancer that begins in the lungs, often due to smoking.",
    "Stroke": "A condition in which poor blood flow to the brain results in cell death.",
    "Thyroid Disease": "Conditions that affect the thyroid gland, which produces hormones that regulate metabolism.",
    "Kidney Disease": "A condition in which the kidneys are damaged and can't filter blood as they should.",
    "Liver Disease": "A condition that impairs the function of the liver.",
    "Sickle Cell Anemia": "A group of disorders that cause red blood cells to become misshapen and break down.",
    "COVID-19": "A respiratory illness caused by the coronavirus SARS-CoV-2.",
    "Ebola": "A rare but severe viral illness that is often fatal, marked by fever, bleeding, and organ failure.",
    "Leukemia": "A type of cancer of the body's blood-forming tissues, including the bone marrow and the lymphatic system.",
    "Gout": "A form of arthritis characterized by severe pain, redness, and tenderness in joints.",
    "Multiple Sclerosis": "A disease in which the immune system eats away at the protective covering of nerves.",
    "Crohn's Disease": "A type of inflammatory bowel disease that causes inflammation of the digestive tract.",
    "COPD": "A chronic inflammatory lung disease that causes obstructed airflow from the lungs.",
    "Epilepsy": "A disorder in which nerve cell activity in the brain is disturbed, causing seizures.",
    "Cholera": "An infectious disease causing severe watery diarrhea, which can lead to dehydration and death.",
    "Meningitis": "An inflammation of the membranes surrounding the brain and spinal cord.",
    "Polio": "A viral disease that can affect nerves and can lead to partial or full paralysis.",
    "Typhoid": "A bacterial infection that can lead to high fever, diarrhea, and vomiting.",
    "Bronchitis": "An inflammation of the lining of your bronchial tubes, which carry air to and from your lungs.",
    "Dermatitis": "A general term that describes inflammation of the skin."
}

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

        sql_insert_query = """
        INSERT INTO tests (test_name, description) 
        VALUES (%s, %s)
        """

        for _ in range(100):
            test_name, description = random.choice(list(medical_diseases.items()))
            
            cursor.execute(sql_insert_query, (test_name, description))

        connection.commit()
        print("100 records inserted successfully into tests table.")

except Error as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
