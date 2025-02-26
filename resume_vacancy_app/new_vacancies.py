'''
import sqlite3
import pandas as pd

# Путь к файлу базы данных
db_path = 'db.sqlite3'
connection = sqlite3.connect(db.sqlite3)


# Чтение данных из CSV файла в DataFrame
df = pd.read_csv('/home/prom/Рабочий стол/perenoc/hh/vacancies.csv')

# Запись данных в таблицу базы данных
df.to_sql('vacancies', connection, if_exists='append', index=False)

connection.commit()
# Закрытие соединения
connection.close()
'''
import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Удаление данных по циклу
for row_id in range(134162):
    cursor.execute("DELETE FROM resume_vacancy_app_vacancy WHERE id = ?", (row_id,))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
