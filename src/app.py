import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Cargar las variables del archivo .env
load_dotenv()

# Función para conectarse a la base de datos
def connect():
    connection_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(connection_string)
    return engine

# Función para leer datos de una tabla y devolver un DataFrame
def read_table(engine, table_name):
    query = f"SELECT * FROM {table_name};"
    with engine.connect() as connection:
        dataframe = pd.read_sql(query, con=connection.connection)
    return dataframe

# Función principal
def main():
    # Conectar a la base de datos
    engine = connect()

    # Leer datos de las tablas
    dataframe_books = read_table(engine, "books")
    dataframe_publishers = read_table(engine, "publishers")
    dataframe_authors = read_table(engine, "authors")
    dataframe_book_authors = read_table(engine, "book_authors")

    # Mostrar datos
    print("Datos de la tabla 'books':")
    print(dataframe_books.head())
    print("Datos de la tabla 'publishers':")
    print(dataframe_publishers.head())
    print("Datos de la tabla 'authors':")
    print(dataframe_authors.head())
    print("Datos de la tabla 'book_authors':")
    print(dataframe_book_authors.head())

    # Visualización: Distribución de ratings de los libros
    plt.figure(figsize=(8, 4))
    sns.histplot(data=dataframe_books, x='rating', bins=10, kde=True)
    plt.title('Distribución de la clasificación de los Libros')
    plt.xlabel('Clasificación')
    plt.ylabel('Frecuencia')
    plt.show()

    # Visualización: Conteo de libros por editorial
    plt.figure(figsize=(8, 4))
    sns.countplot(data=dataframe_books, x='publisher_id')
    plt.title('Conteo de Libros por Editorial')
    plt.xlabel('ID de Editorial')
    plt.ylabel('Cantidad de Libros')
    plt.show()

    # Visualización: Conteo de libros por autor
    plt.figure(figsize=(8, 4))
    sns.countplot(data=dataframe_book_authors, x='author_id')
    plt.title('Conteo de Libros por Autor')
    plt.xlabel('ID de Autor')
    plt.ylabel('Cantidad de Libros')
    plt.show()

# Ejecutar la función principal
if __name__ == "__main__":
    main()