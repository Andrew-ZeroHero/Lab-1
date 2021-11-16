import zipfile
import os
import hashlib
import re
import requests

# Задание №1 - Извлечение файлов из архива в директорию

directory_to_extract_to = 'D:\\Saves from browser\\Extracted'
arch_file = 'D:\\Saves from browser\\tiff-4.2.0_lab1.zip'
f_zip = zipfile.ZipFile(arch_file)
f_zip.extractall(directory_to_extract_to)
f_zip.close()

# Задание №2.1 - Получить список файлов (полный путь) формата txt, находящихся в directory_to_extract_to. Сохранить полученный список в txt_files

txt_files = []
for root, dirs, files in os.walk(directory_to_extract_to):
  for file in files:
    if file.find(".txt"):
      txt_files.append(os.path.join(root, file))
print(txt_files)
print('~~~~~~~~~~~~~~' * 5)

# Задание №2.2 - Получить значения MD5 хеша для найденных файлов и вывести полученные данные на экран.

for file in txt_files:
  target_file = file
  file_data = open(target_file, 'rb').read()
  result = hashlib.md5(file_data).hexdigest()
  print(result)

# Задание №3 - Найти файл, хэш которого равен: "4636f9ae9fef12ebd56cd39586d33cfb"

req_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
req_file = ''
req_file_data = ''
for root, dirs, files in os.walk(directory_to_extract_to):
  for file in files:
    check_file = os.path.join(root, file)
    file_data = open(check_file, 'rb').read()
    hash_returned = hashlib.md5(file_data).hexdigest()
    if req_hash == hash_returned:
      req_file = os.path.join(root, file)
      req_file_data = file_data
print(req_file)
print(req_file_data)

# Задание №4 - Ниже представлен фрагмент кода парсинга HTML страницы с помощью регулярных выражений. Возможно выполнение этого задания иным способом (например, с помощью сторонних модулей).

r = requests.get(req_file_data)
result_dct = {}
counter = 0
headers = []
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
for line in lines:
    if counter == 0:
        headers = re.findall('([А-ЯЁа-яё]+ ?[А-ЯЁа-яё]*)+', line)
        counter += 1
    else:
        tmp = re.sub('<.*?>', ';', line)
        tmp = re.sub(r'(\(\+\d+\s?\d*\))', ';', tmp)
        tmp = re.sub('(;)+', ';', tmp)
        tmp = re.sub('(_)', '-1', tmp)
        tmp = re.sub(r'(\*)', '', tmp)
        tmp = tmp[3:].strip()
        tmp = re.sub(r';$', '', tmp)
        tmp = re.sub(r'^;', '', tmp)
        tmp = re.sub(r'\xa0', '', tmp)
        tmp_split = tmp.split(';')

        country_name = tmp_split[0]

        col1_val = tmp_split[1]
        col2_val = tmp_split[2]
        col3_val = tmp_split[3]
        col4_val = tmp_split[4]
        counter += 1

        result_dct[country_name] = {}
        result_dct[country_name][headers[0]] = int(col1_val)
        result_dct[country_name][headers[1]] = int(col2_val)
        result_dct[country_name][headers[2]] = int(col3_val)
        result_dct[country_name][headers[3]] = int(col4_val)

        print(country_name, result_dct[country_name])
print('~~~~~~~~~~~~~~' * 5)

# Задание №5 - Запись данных из полученного словаря в файл

output = open('data.csv', 'w')
headline = '; '.join(headers)
output.write('Страна;' + headline + '\n')
for key in result_dct.keys():
    values_of_dict = result_dct[key].values()
    row = '; '.join(map(str, values_of_dict))
    output.write(key + ';' + row + '\n')
output.close()

# Задание №6 - Вывод на экран для указанной страны

target_country = input("Введите название страны: ")
f = False
for key in result_dct.keys():
    if key.lower() == target_country.lower():
        print(key + ': ' + str(result_dct[key]))
        f = True
if not f:
    print('Данной страны нет в списке') 
