import struct
import csv

def extract_texts(binary_file, csv_file):
    """
    Извлекает тексты из бинарного файла и записывает их в CSV-файл.

    Args:
        binary_file (str): Путь к бинарному файлу.
        csv_file (str): Путь к CSV-файлу для записи результатов.
    """

    with open(binary_file, "rb") as bin_file, open(csv_file, "w", newline="", encoding="utf-8") as csv_file:
        # Пропускаем первые 8 байт
        bin_file.seek(8)

        # Считываем количество текстов
        text_count = struct.unpack("<I", bin_file.read(4))[0]
        #print(text_count)

        # Создаем объект CSV-писателя
        writer = csv.writer(csv_file)

        # Записываем заголовок CSV-файла
        writer.writerow(["id_текста", "текст"])

        # Считываем информацию о текстах
        for _ in range(text_count):
            
            # Считываем ID и оффсет текста
            text_id, text_offset = struct.unpack("<II", bin_file.read(8))

            current_offset = bin_file.tell()

            # Перемещаемся к началу текста
            bin_file.seek(text_offset)

            # Считываем текст
            text = ""
            byte = bin_file.read(1)
            while byte != b"\x00":  # Читаем до нулевого байта
                text += byte.decode("latin-1")
                byte = bin_file.read(1)

            # Записываем информацию в CSV-файл
            writer.writerow([text_id, text])

            bin_file.seek(current_offset)


if __name__ == "__main__":
    # Замените эти значения на ваши пути к файлам
    binary_file_path = "file_3735885291.dat" 
    csv_file_path = "extracted_texts.csv"

    extract_texts(binary_file_path, csv_file_path)