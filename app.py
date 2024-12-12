import psycopg2
from psycopg2 import sql

# Параметри підключення до вашої бази даних
host = 'junction.proxy.rlwy.net'
port = '19910'  # порт з Railway
database = 'RailwayDB'  # ім'я бази даних
user = 'postgres'  # користувач
password = 'ygenbXELPjFcAdfMKwzQwfXmPGDJIAqu'  # пароль з Railway

# Створення з'єднання з базою даних
try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    
    cursor = connection.cursor()

    # Перевірка, чи існує таблиця
    cursor.execute("""
    SELECT to_regclass('public.users');
    """)
    table_exists = cursor.fetchone()[0]
    
    if table_exists:
        print("Таблиця 'users' вже існує.")
    else:
        print("Таблиця 'users' не знайдена.")
        # Можна створити таблицю, якщо вона не існує (необов'язково, якщо ви впевнені, що вона є)
        create_table_query = '''
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            name VARCHAR(100),
            age INT,
            email VARCHAR(100),  -- Додав стовпець email
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        cursor.execute(create_table_query)
        connection.commit()
        print("Таблиця успішно створена!")

    # Перевірка структури таблиці і додавання стовпців, якщо їх немає
    cursor.execute("""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = 'users';
    """)
    
    columns = [column[0] for column in cursor.fetchall()]
    if 'name' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN name VARCHAR(100);')
        print("Стовпець 'name' додано.")
    if 'age' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN age INT;')
        print("Стовпець 'age' додано.")
    if 'username' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN username VARCHAR(100) NOT NULL;')
        print("Стовпець 'username' додано.")
    if 'email' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN email VARCHAR(100);')  # Додав email
        print("Стовпець 'email' додано.")
    
    connection.commit()

    # Додавання нового запису з email
    insert_query = '''
    INSERT INTO users (username, name, age, email) VALUES (%s, %s, %s, %s);
    '''
    cursor.execute(insert_query, ('jane_smith', 'Jane Smith', 30, 'jane.smith@example.com'))
    connection.commit()
    print("Новий запис успішно доданий!")

    # Отримання та виведення даних з таблиці
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except Exception as error:
    print(f"Помилка при підключенні або виконанні запиту: {error}")

finally:
    # Закриття курсору та з'єднання
    if cursor:
        cursor.close()
    if connection:
        connection.close()
