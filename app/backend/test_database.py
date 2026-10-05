from database import get_connection


connection = get_connection()


if connection:

    print("======================================")
    print("DATABASE CONNECTION SUCCESSFUL")
    print("======================================")

    cursor = connection.cursor()

    cursor.execute("SELECT current_database();")

    result = cursor.fetchone()

    print("Connected database:", result[0])

    cursor.close()
    connection.close()

else:

    print("======================================")
    print("DATABASE CONNECTION FAILED")
    print("======================================")