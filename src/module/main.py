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

def write_files(redy_data, file_name_buf):
    buffer = str(file_name_buf).split(".")
    try:
        i = 0
        while(i < 100):
            if(i != 0):
                file_name = ""
                if  len(buffer) > 1:
                    file_name = buffer[0] + f"({i})." + buffer[1]
                else:
                    file_name = buffer[0] + f"({i})"
            else:
                if  len(buffer) > 1:
                    file_name = buffer[0] + "." + buffer[1]
                else:
                    file_name = buffer[0]
            f = open(file_name,'r')
            f.close()
            i = i + 1
        print(f"не удалось записать в файл1\n {e}")
    except Exception as e:
        try:
             with open(file_name,'w',encoding="utf-8") as f:
                f.write(redy_data)
                print("файл успешно создан")
        except Exception as ex:
            print(f"не удалось записать в файл2\n {ex}")

    return 0

def parsing(raw_data, file_name = "raw_equation.txt"):
    regx1 = r'<math .*?>([\s\S]*?)</math>'
    stack = []
    buffer = []
    write_data = ""
    
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
            flag = 1
            sumbol = IdentSumbol(i)

            
            if sumbol  == "{":
                flag = 0
                stack.append("")
            elif  sumbol  == "}": 
                if len(stack) != 0:
                    sumbol = sumbol + stack.pop()
            elif sumbol  == "(":
                stack.append("")
            elif sumbol  == ")":
                if len(stack) != 0:
                    sumbol = sumbol + stack.pop()
            elif ((sumbol == "-")or(sumbol =="+")or(sumbol =="\\cdot")or(sumbol =="^")):
                stack.append(sumbol)
                sumbol = ""
            elif (sumbol =="\\frac"):
                stack.append("")
            elif sumbol =="\\sqrt[":
                stack.append("]")
            elif sumbol =="equal":
                stack.append("=")
                sumbol = ""
            elif flag == 1:
                if len(stack) != 0:
                    sumbol = sumbol + stack.pop()



            result = result + sumbol     

                    
            print(f"{k} {i}")
            k = k + 1
        result = re.sub("=+","=",result)
        result = re.sub("^=+","",result)
        result = re.sub("explicit.*?{","{",result)
        result = re.sub("solve.*?{","{",result)
        print(result)
        write_data = write_data +"\\[" + result + "\\]\n"
        result = ""
        stack.clear()

        j = j + 1
    
    write_files(write_data, file_name)
    return 0 


def IdentSumbol(i):
    sumbol_round = 3
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
        sumbol ="\\sqrt["
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
    elif  re.search ("<ml:equal/>",i):
        sumbol ="equal"     
    else:
         sumbol =''      
    return sumbol 


def main (argv = []):

    if len(argv) == 1:
        raw_data = ReadFiles (argv[1])
        parsing(raw_data)
    elif len(argv) > 2:
                raw_data = ReadFiles (argv[1])
                parsing(raw_data, argv[2])
    else:
        print("Введите путь до разбираемого файла")

    return 0


if __name__ == "__main__":
    main(argv)