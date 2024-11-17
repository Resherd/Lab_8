import logging
from datetime import date
from prettytable import PrettyTable
from sqlalchemy import create_engine, text, Column, String, Integer, Float, ForeignKey, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect

# Логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

LOGGER.info("Start operations")

# Визначаємо двигун підключення до PostgreSQL
password = "postgres"
engine = create_engine(f'postgresql://postgres:{password}@postgres:5432/pharmacy')

# Створюємо сесію
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Визначаємо моделі (таблиці)
class Medicine(Base):
    __tablename__ = 'medicine'
    registration_number = Column(Integer, primary_key=True)  # Реєстраційний номер ліки
    name = Column(String(50))  # Назва ліки
    manufacture_date = Column(Date)  # Дата виготовлення
    shelf_life_days = Column(Integer)  # Термін зберігання (кількість днів)
    group_name = Column(String(50))  # Група (Протизапальне, Знеболююче тощо)
    price = Column(Float)  # Ціна
    prescription_required = Column(Boolean)  # Відпускається за рецептом лікаря (Так/Ні)

class Supplier(Base):
    __tablename__ = 'suppliers'
    supplier_code = Column(Integer, primary_key=True)  # Код постачальника
    supplier_name = Column(String(100))  # Назва постачальника
    address = Column(String(255))  # Адреса
    phone = Column(String(15))  # Телефон (маска вводу)
    contact_person = Column(String(100))  # Контактна особа
    location = Column(String(50))  # Розташування (Україна, інша країна)

class Deliveries(Base):
    __tablename__ = 'deliveries'
    delivery_id = Column(Integer, primary_key=True)  # Код поставки
    delivery_date = Column(Date)  # Дата поставки
    medicine_registration_number = Column(Integer, ForeignKey('medicine.registration_number'))  # Номер ліки
    quantity = Column(Integer)  # Кількість ліків, які були поставлені
    supplier_code = Column(Integer, ForeignKey('suppliers.supplier_code'))  # Код постачальника

# Перевірка на існування таблиць
inspector = inspect(engine)
if "medicine" in inspector.get_table_names() and "suppliers" in inspector.get_table_names() and "deliveries" in inspector.get_table_names():
    LOGGER.info("Tables exist")
else:
    LOGGER.info("Create all tables operations")
    Base.metadata.create_all(engine)

# Визначення даних
medicine_data = [
    ('Aspirin', '2024-01-10', 365, 'Anti-inflammatory', 120.50, True),
    ('Paracetamol', '2023-12-05', 730, 'Painkiller', 85.00, True),
    ('Ibuprofen', '2024-02-15', 540, 'Painkiller', 95.00, False),
    ('Metformin', '2023-11-25', 365, 'Diabetes', 150.00, True),
    ('Atorvastatin', '2023-10-30', 730, 'Cardiovascular', 200.00, True),
    ('Amoxicillin', '2023-08-20', 365, 'Antibiotic', 180.00, False),
    ('Omeprazole', '2024-01-01', 365, 'Gastrointestinal', 130.00, True),
    ('Losartan', '2024-04-15', 365, 'Cardiovascular', 175.00, True),
    ('Hydrochlorothiazide', '2023-09-10', 365, 'Diuretic', 145.00, False),
    ('Levothyroxine', '2023-12-25', 730, 'Hormonal', 210.00, True),
    ('Vitamin C', '2024-03-01', 180, 'Supplement', 50.00, False),
    ('Cetirizine', '2023-11-10', 365, 'Antihistamine', 110.00, False),
    ('Lisinopril', '2024-07-10', 540, 'Cardiovascular', 120.00, True),
    ('Simvastatin', '2023-06-25', 730, 'Cardiovascular', 190.00, True),
    ('Ranitidine', '2023-10-05', 365, 'Gastrointestinal', 85.00, False)
]

suppliers_data = [
    (1, 'PharmaCo', '123 Main St', '+380501234567', 'John Doe', 'Ukraine'),
    (2, 'MedSupply', '456 Elm St', '+380672345678', 'Jane Smith', 'Other Country'),
    (3, 'HealthCorp', '789 Oak St', '+380633456789', 'Mary Johnson', 'Ukraine'),
    (4, 'Wellness Ltd.', '321 Pine St', '+380501234890', 'David Lee', 'Other Country'),
    (5, 'PharmX', '654 Maple St', '+380505678901', 'Linda Brown', 'Ukraine'),
    (6, 'Global Med', '987 Birch St', '+380673456012', 'James Wilson', 'Other Country'),
    (7, 'MediCare', '112 Cedar St', '+380501234987', 'Emily Davis', 'Ukraine'),
    (8, 'BioPharma', '221 Spruce St', '+380672345321', 'George Miller', 'Other Country'),
    (9, 'MedicSupply', '333 Redwood St', '+380633456654', 'Patricia Taylor', 'Ukraine'),
    (10, 'CureCorp', '444 Palm St', '+380501234321', 'Michael Anderson', 'Other Country'),
    (11, 'LifeMed', '555 Birchwood St', '+380672345432', 'Sarah Harris', 'Ukraine'),
    (12, 'NaturePharma', '666 Fir St', '+380633456123', 'Robert Clark', 'Other Country'),
    (13, 'MedTech', '777 Willow St', '+380505678432', 'Laura Lewis', 'Ukraine'),
    (14, 'Healix', '888 Cedarwood St', '+380501234654', 'Daniel Young', 'Other Country'),
    (15, 'MaxMed', '999 Redwood Ave', '+380672345543', 'Susan King', 'Ukraine')
]

deliveries_data = [
    (1, '2024-02-10', 500, 1),
    (2, '2024-02-12', 600, 2),
    (3, '2024-02-14', 450, 3),
    (4, '2024-02-16', 700, 4),
    (5, '2024-02-18', 350, 5),
    (6, '2024-02-20', 520, 6),
    (7, '2024-02-22', 480, 1),
    (8, '2024-02-24', 650, 2),
    (9, '2024-02-26', 400, 3),
    (10, '2024-02-28', 300, 4),
    (11, '2024-03-02', 720, 5),
    (12, '2024-03-04', 500, 6),
    (13, '2024-03-06', 530, 1),
    (14, '2024-03-08', 470, 2),
    (15, '2024-03-10', 600, 3)
]

# Вставка даних
def insert_data():
    try:
        # Ліки
        for idx, med in enumerate(medicine_data, start=1):
            session.add(Medicine(
                registration_number=idx,
                name=med[0],
                manufacture_date=med[1],
                shelf_life_days=med[2],
                group_name=med[3],
                price=med[4],
                prescription_required=med[5]
            ))
        session.commit()

        # Постачальники
        for supplier in suppliers_data:
            session.add(Supplier(
                supplier_code=supplier[0],
                supplier_name=supplier[1],
                address=supplier[2],
                phone=supplier[3],
                contact_person=supplier[4],
                location=supplier[5]
            ))
        session.commit()

        # Поставки
        for delivery in deliveries_data:
            session.add(Deliveries(
                delivery_id=delivery[0],
                delivery_date=delivery[1],
                quantity=delivery[2],
                supplier_code=delivery[3],
                medicine_registration_number=delivery[0]  # Забезпечуємо, щоб реєстраційний номер ліків відповідав
            ))
        session.commit()
    except IntegrityError as e:
        session.rollback()
        LOGGER.error(f"Error while inserting data: {e}")

# Перевірка даних у таблицях
def check_table_data():
    tables = ['medicine', 'suppliers', 'deliveries']
    for table in tables:
        result = execute_query(f"SELECT COUNT(*) FROM {table}")
        LOGGER.info(f"Total rows in {table}: {result[0][0] if result[0] else 0}")

# Запити
def execute_query(query, params=None):
    with engine.connect() as connection:
        result = connection.execute(text(query), params)
        return result.fetchall(), result.keys()

def print_results(title, results):
    rows, headers = results
    if rows:
        table = PrettyTable(headers)
        table.align = "l"
        for row in rows:
            table.add_row(row)
        LOGGER.info(f"\n{title}:\n{table}")
    else:
        LOGGER.info(f"\n{title}: No results found")

# Приклад виконання запитів
def run_queries():
    # 1. Ліки, які відпускаються за рецептом
    query1 = "SELECT * FROM medicine WHERE prescription_required = TRUE ORDER BY name"
    print_results("Medicines requiring prescription", execute_query(query1))

    # 2. Ліки за групою (наприклад, 'Painkiller')
    query2 = "SELECT * FROM medicine WHERE group_name = :group_name"
    print_results("Medicines in group Painkiller", execute_query(query2, {'group_name': 'Painkiller'}))

    # 3. Вартість кожної поставки
    query3 = """
    SELECT d.delivery_id, m.name, d.quantity, (d.quantity * m.price) AS total_cost
    FROM deliveries d
    JOIN medicine m ON d.medicine_registration_number = m.registration_number
    """
    print_results("Delivery costs", execute_query(query3))

    # 4. Загальна сума грошей для кожного постачальника
    query4 = """
    SELECT s.supplier_name, SUM(d.quantity * m.price) AS total_paid
    FROM deliveries d
    JOIN suppliers s ON d.supplier_code = s.supplier_code
    JOIN medicine m ON d.medicine_registration_number = m.registration_number
    GROUP BY s.supplier_name
    """
    print_results("Total payments to suppliers", execute_query(query4))

    # 5. Кількість поставок для кожної групи ліків
    query5 = """
    SELECT m.group_name, 
       SUM(CASE WHEN s.location = 'Ukraine' THEN 1 ELSE 0 END) AS Domestic, 
       SUM(CASE WHEN s.location = 'Other Country' THEN 1 ELSE 0 END) AS International 
    FROM deliveries d 
    JOIN suppliers s ON d.supplier_code = s.supplier_code 
    JOIN medicine m ON d.medicine_registration_number = m.registration_number 
    GROUP BY m.group_name
    """
    print_results("Deliveries by group and supplier location", execute_query(query5))

    # 6. Остання дата придатності для кожної ліки
    query6 = """
        SELECT registration_number, name, (manufacture_date + INTERVAL '1 day' * shelf_life_days) AS expiration_date
        FROM medicine
    """
    print_results("Expiration dates for each medicine", execute_query(query6))

# Основна функція
def main():
    insert_data()
    check_table_data()
    run_queries()

if __name__ == "__main__":
    main()
