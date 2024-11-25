import mysql.connector

DB_NAME = 'Talabalar_Tizimi2'

##Ushbularni o'zinikiga o'zgartiring
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '12345'


def init_db():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            auth_plugin='mysql_native_password'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            create_database_script = f"""
                CREATE DATABASE IF NOT EXISTS {DB_NAME};
            """
            cursor.execute(create_database_script)
            connection.commit()

            connection.database = DB_NAME

            create_students_table_script = """
                CREATE TABLE IF NOT EXISTS students(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    full_name VARCHAR(100) NOT NULL,
                    age INT NOT NULL,
                    phone_number VARCHAR(100) NOT NULL,
                    course VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    location VARCHAR(100) NOT NULL
                );
            """
            cursor.execute(create_students_table_script)
            connection.commit()
    except mysql.connector.Error as e:
        print(f"Mysql ma'lumotlar bazasiga ulanishda xatolik yuz berdi: {e}")
    except Exception as e:
        print(f"Database yaratishda xatolik yuz berdi: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

    return connection

