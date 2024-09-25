import struct
import zlib
import os

def unpack_vt7a(archive_path, output_dir):
    #  Открываем архив для чтения
    with open(archive_path, 'rb') as archive_file:
        # Читаем заголовок
        header = archive_file.read(16)
        signature, version, unknown, num_files = struct.unpack("<4sI4sI", header)

        current_offset = archive_file.tell()
        #  Обрабатываем информацию о каждом файле
        for _ in range(num_files):
            
            archive_file.seek(current_offset)
            # Читаем информацию о файле из каталога
            file_info = archive_file.read(16)

            unknown, file_offset, decompressed_length, compressed_length = struct.unpack("<4I", file_info)
            
            current_offset = archive_file.tell()
            #  Перемещаем указатель к данным файла
            archive_file.seek(file_offset)

            # Читаем данные файла
            data = archive_file.read(compressed_length)

            #  Разархивируем файл, если он сжат
            if compressed_length > 0:
                data = zlib.decompress(data)

            # Сохраняем файл
            file_name = f"file_{unknown}.dat"  #  Пример имени файла 
            with open(os.path.join(output_dir, file_name), 'wb') as output_file:
                output_file.write(data)
            

#  Пример использования
unpack_vt7a("text.vt7a", "text")