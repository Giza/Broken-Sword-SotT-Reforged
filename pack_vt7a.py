import struct
import zlib
import os

def pack_vt7a(input_dir, archive_path):
    #  Получаем список файлов в директории
    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    num_files = len(files)

    #  Создаем заголовок
    signature = b"VT7A"
    version = 2
    unknown = b"\x5E\x0B\x99\x8F"
    header = struct.pack("<4sI4sI", signature, version, unknown, num_files)

    #  Открываем архив для записи
    with open(archive_path, 'wb') as archive_file:
        #  Записываем заголовок
        archive_file.write(header)

        #  Список для хранения сжатых данных
        compressed_data_list = []

        #  Обрабатываем каждый файл
        file_offset = len(header)*8
        for i, file_name in enumerate(files):
            file_number = int(file_name.split("_")[1].split(".")[0])
            file_path = os.path.join(input_dir, file_name)

            #  Считываем файл
            with open(file_path, 'rb') as file_to_pack:
                data = file_to_pack.read()
                compressed_data = zlib.compress(data)  #  Сжатие файла
                compressed_length = len(compressed_data)
                decompressed_length = len(data)

            #  Записываем информацию о файле
            file_info = struct.pack("<4I", file_number, file_offset, decompressed_length, compressed_length)

            archive_file.write(file_info)

            #  Записываем данные файла
            compressed_data_list.append(compressed_data)

            #  Обновляем смещение для следующего файла
            file_offset += len(file_info)-16 + compressed_length
        for i, compressed_data in enumerate(compressed_data_list):
            archive_file.write(compressed_data)
#  Пример использования
pack_vt7a("text", "text.vt7a")