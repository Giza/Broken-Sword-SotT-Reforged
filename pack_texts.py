import struct
import csv

def pack_texts(csv_file, binary_file):
    """
    Упаковывает тексты из CSV-файла в бинарный файл.

    Args:
        csv_file (str): Путь к CSV-файлу с текстами.
        binary_file (str): Путь к бинарному файлу для записи.
    """

    with open(csv_file, "r", newline="", encoding="utf-8") as csv_file, open(binary_file, "wb") as bin_file:
        bin_file.write(b"\x54\x45\x58\x54")
        # Записываем первые 8 байт (зарезервированные)
        bin_file.write(b"\x00" * 4)

        # Считываем данные из CSV
        reader = csv.reader(csv_file)

        # Записываем количество текстов
        text_count = len(list(reader))
        bin_file.write(struct.pack("<I", text_count-1))

        # Возвращаемся к началу файла
        csv_file.seek(0)
        next(reader)  # Пропускаем заголовок

        text_list = []

        # Текущий оффсет в бинарном файле
        current_offset = bin_file.tell()
        file_offset=(text_count-1)*8+12
        # Записываем тексты
        for row in reader:
            text_id, text, text_tl = row

            # Записываем ID и оффсет текста
            bin_file.write(struct.pack("<II", int(text_id), file_offset))
            
            # Записываем текст с нулевым байтом в конце
            texts = text_tl.encode("utf-8")+b"\x00"
            text_list.append(texts)

            # Обновляем текущий оффсет
            file_offset += len(texts)

        for i, text in enumerate(text_list):
            bin_file.write(text)

if __name__ == "__main__":
    # Замените эти значения на ваши пути к файлам
    csv_file_path = "extracted_texts.csv"
    binary_file_path = "file_3735885291.dat" 

    pack_texts(csv_file_path, binary_file_path)