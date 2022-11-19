from sys import argv
import re

def ReadFiles (name_file):

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
    regx1 = r'<math .*?>([\s\S]*?)</math>'
    stack = []
    buffer = []
    
    regx_str = re.findall(regx1,raw_data)
    result = ''

    if len(regx_str) == 0:
        print("уравнения не найдены")
        return 1

    #обход блоков уравнений
    j = 0
    for i in regx_str:
        
        #regx_str[j] = i.replace('\t', '')
        
        i = re.search("<ml:id.*?>(.*?)</ml:id>",regx_str[j])

        print(f"\n\n                        блок {j}") 
        #result = i.group(1)
        print(f"Переменная: {i.group(1)}=\n")

        buffer = str(regx_str[j]).split("\n")

        #построковый разбор
        k = 0
        flag = 0
        lock = 0
        for i in buffer:
            sumbol = IdentSumbol(i)

            
            if sumbol  == "{":
                flag = 0
            elif  sumbol  == "}" and lock == 0: 
                if len(stack) != 0:
                    sumbol = sumbol + stack.pop()
                flag = 0
            elif sumbol  == "(":
                lock = 1
            elif sumbol  == ")":
                lock = 0
            elif ((sumbol == "-")or(sumbol =="+")or(sumbol =="\\cdot")or(sumbol =="^")):
                stack.append(sumbol)
                sumbol = ""
                flag = 1
            elif (sumbol =="\\frac")or(sumbol =="\\sqrt"):
                stack.append("")
            elif flag == 1 and sumbol !=")":
                flag = 0
                sumbol = sumbol + stack.pop()



            result = result + sumbol     

                    
            print(f"{k} {i}")
            k = k + 1
        print(result)
        result = ""

        j = j + 1


def IdentSumbol(i):
    str(i)
    sumbol =''
    if  re.search ("<ml:apply>",i):
        sumbol = "{"                   
    elif re.search ("<ml:minus/>",i): 
        sumbol ="-"
    elif re.search ("<ml:plus/>",i):
        sumbol ="+"
    elif re.search ("<ml:mult/>",i): 
        sumbol ="\cdot"
    elif re.search ("<ml:div/>",i):
        sumbol ="\\frac"
    elif  re.search ("</ml:apply>",i):
        sumbol ="}"
    elif  re.search ("<ml:parens>",i):
        sumbol ="("
    elif  re.search ("</ml:parens>",i):
        sumbol =")"
    elif re.search ("<ml:pow/>",i):
        sumbol ="^"
    elif re.search ("<ml:sqrt/>",i):
        sumbol ="\\sqrt"
    elif re.search ("<ml:nthRoot/>",i):
        sumbol ="\\sqrt"
    elif  re.search ("<ml:command>",i):
        sumbol ="="
    elif  re.search ("<ml:real>.*?</ml:real>",i):
        sumbol = "{" + re.search ("<ml:real>(.*?)</ml:real>",i).group(1) + "}" 
    elif  re.search ("<ml:id.*?>.*?</ml:id>",i):
        sumbol = re.search ("<ml:id.*?>(.*?)</ml:id>",i).group(1) 
    elif  re.search ("<ml:symEval.*?>",i):
        sumbol = "="
    elif re.search ("<ml:eval.*?>",i): 
        sumbol = "="       
    elif  re.search ("<result.*?>",i):
        sumbol ="=" 
    else:
         sumbol =''      
    return sumbol 


def main (argv = []):

    if len(argv) > 1:
        raw_data = ReadFiles (argv[1])
        parsing(raw_data)
    else:
        print("Введите путь до разбираемого файла")

    return 0


if __name__ == "__main__":
    main(argv)