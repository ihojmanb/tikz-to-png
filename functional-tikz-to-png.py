#   Functional Programming version of tikz-to-png
import re, os, sys, unittest

def make_directory(path):
    try:
        os.mkdir(path)
    except OSError as error: 
        print(error)

"""given a TeX file, returns every line of code from start to (including)
'\\begin{document}. Return match object from regex'"""
def get_preamble(tex_file):
    preamble_pattern = r"(.+?)\\begin\{document\}"
    preamble_obj = re.compile(preamble_pattern, re.DOTALL)
    preamble = preamble_obj.match(tex_file)
    return preamble

"""extracts every tikz figure found in TeX file
Return match object from regex """
def get_tikz_figures(tex_file):
    #patron que quiero encontrar en el archivo
    regex_pattern = r"\\begin\{tikzpicture\}(.+?)\\end\{tikzpicture\}"
    #regex pattern compiled into a regex object
    regex_obj = re.compile(regex_pattern, re.DOTALL)
    #match object
    tikz_match_obj = regex_obj.finditer(tex_file)
    return tikz_match_obj

"""takes a figure (regex match object) 
Returns figure name"""
def getTikzFigureName(figure):
    name_pattern = r"%name=.+\s"
    #largo de %name= para poder tomar el nombre en la pos. correcta
    prefix_length = len("%name=")
    name_obj = re.compile(name_pattern)
    name_match = name_obj.search(figure.group())
    file_name = "{}".format(name_match.group()[prefix_length:-1])
    return(file_name)

def writeFigurefile(latex_file, absolute_file_name, preamble_str, tikz_position):
    end_document = "\\end{document}"
    with open("{}.tex".format(absolute_file_name), "w+") as new_file:
        new_file.write(preamble_str.group())
        new_file.write("\n")
        new_file.write(latex_file[tikz_position[0]:tikz_position[1]])
        new_file.write("\n")
        new_file.write(end_document)

def convertTikzToPng(png_dir, figure_name):
    os.chdir(png_dir)
    os.system("pdflatex {}.tex".format(figure_name))
    os.system("pdftops -eps {}.pdf".format(figure_name))
    os.system("convert -density 200 {figure_name}.eps {figure_name}.png".format(figure_name = figure_name))
def main():
    png_dir = "png_figures"
    png_dir = os.path.join(os.getcwd(), png_dir)
    make_directory(png_dir)
    input_file = sys.argv[1]
    try:
        with open(input_file, 'r') as file:
        # 0. leemos el archivo de texto
            latex_file = file.read()
            
        # 1 . encontramos el preambulo del documento Tex
            preamble = get_preamble(latex_file)
            if preamble:
                print('preambulo encontrado:', preamble.span())
            else:
                print('no hay match para preambulo')
        # 2. busquemos los dibujos tikz
            tikz_figures = get_tikz_figures(latex_file)
            
            if tikz_figures: 
        # 3. encontremos el nombre de la figura
                for _, figure in enumerate(tikz_figures):
                    tikz_position = figure.span()
                    figure_name = getTikzFigureName(figure)
                    print('figure name: ', figure_name)
                    absolute_figure_name = os.path.join(png_dir, figure_name)
        # 4. crear nuevos archivos
                    writeFigurefile(latex_file,absolute_figure_name, preamble, tikz_position)
        #   nos cambiamos al directorio png_figures para ejecutar los comandos bash
                    convertTikzToPng(png_dir, figure_name)

            else:
                print('No match')
    except FileNotFoundError:
        print("el archivo '{}' no existe. Por favor vuelve a intentarlo, quizás escribiste mal su nombre.".format(input_file))

if __name__ == '__main__':
    main()

