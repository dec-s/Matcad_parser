from sys import argv
import re

def read_files (name_file):

    try:
        with open(name_file,'r',encoding="utf-8") as file:
            raw_data = file.read()
    except Exception as e:
        print("Ошибка открытия файла:", e)
        exit()

    return raw_data

def write_files(redy_data):
    return 0

def parsing(raw_data):
    regx1 = r'<math [\s\S]*?</math>'
    
    result = re.findall(regx1,raw_data)

    j = 0
    for i in result:
        
        result[j] = i.replace('\t', '')
        print(f"\nблок {j}\n\n",result[j])
        
        j = j + 1


      

    
    return result 


def main (argv = []):

    if len(argv) > 1:
        raw_data = read_files (argv[1])
        parsing(raw_data)
    else:
        print("Введите путь до разбираемого файла")

    return 0


if __name__ == "__main__":
    main(argv)