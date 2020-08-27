import re, os, sys
png_dir = "png_figures"
png_dir = os.path.join(os.getcwd(), png_dir)
try:
    os.mkdir(png_dir)
except OSError as error: 
    print(error) 
input_file = sys.argv[1]
print(input_file)
with open(input_file, 'r') as f:
    # 0. leemos el archivo de texto
    read_data = f.read()
    end_document = "\\end{document}"
    # 1 . encontramos el preambulo del documento Tex
    preambulo_pattern = r"(.+?)\\begin\{document\}"
    preambulo_obj = re.compile(preambulo_pattern, re.DOTALL)
    preambulo_match = preambulo_obj.match(read_data)
    if preambulo_match:
        print('preambulo encontrado:', preambulo_match.span())
    else:
        print('no hay match para preambulo')

    # 2. busquemos los dibujos tikz
    #patron que quiero encontrar en el archivo
    regex_pattern = r"\\begin\{tikzpicture\}(.+?)\\end\{tikzpicture\}"
    #regex pattern compiled into a regex object
    regex_obj = re.compile(regex_pattern, re.DOTALL)
    #match object
    m = regex_obj.finditer(read_data)
    if m:
    # 3. encontremos el nombre de la figura
        for i, match_obj in enumerate(m):
            span = match_obj.span()
            name_pattern = r"%name=.+\s"
            #largo de %name= para poder tomar el nombre en la pos. correcta
            prefix_length = len("%name=")
            #print(match_obj.group())
            name_obj = re.compile(name_pattern)
            name_match = name_obj.search(match_obj.group())
            # print(name_match.span())
            file_name = "{}".format(name_match.group()[prefix_length:-1])
            complete_file_name = os.path.join(png_dir, file_name)
            print(file_name)
    # 4. crear nuevos archivos
            with open("{}.tex".format(complete_file_name), "w+") as new_file:
                new_file.write(preambulo_match.group())
                new_file.write("\n")
                new_file.write(read_data[span[0]:span[1]])
                new_file.write("\n")
                new_file.write(end_document)
    #   nos cambiamos al directorio png_figures para ejecutar los comandos bash
            os.chdir(png_dir)
            os.system("pdflatex {}.tex".format(file_name))
            os.system("pdftops -eps {}.pdf".format(file_name))
            os.system("convert -density 200 {}.eps {}.png".format(file_name, file_name))

    else:
        print('No match')



