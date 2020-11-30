
import png, subprocess
#from  import run, PIPE

#import numpy

#Le symbole de la fin du message 
END_OF_MESSAGE = "#FIN#"
# le decalage de pixel lors du hidding et du finding pour le 'effet ne soit pas si visible
OFFSET = 600

a = [
        [1,3, 2, 3], [2,4,3, 4]
    ]
def size_2D(array_2D):
    """
    docstring
    Fonction qui permet de retrouver le nombre d'element d'un array de 2D
    (list(list))-> number
    >>> a = [
    ...         [1,3], [2,4], [3, 4]
    ...     ]
    >>> size_2D(a)
    6
    >>> a = [
    ...         [1,3, 2, 3], [2,4,3, 4]
    ...     ]
    >>> size_2D(a)
    8
    >>> a = [
    ...         [1], [2]
    ...     ]
    >>> size_2D(a)
    2
    >>> 
    """
    return len(array_2D)*len(array_2D[0])

def check(png_2d, msg):
    """
    docstring
    Fonction qui permet de verifier qu'un message peut être caché dans un image

    (Array_2D, str) raise Exception -> NoneType
    """
    if (size_2D(png_2d)/OFFSET) <= (len(msg) + len(END_OF_MESSAGE))*2 :
        raise Exception("Message Trop Long !")

def save_to_png(png_2d, path, info):
    """
    docstring
    Focntion qui permet de sauvegarder un 2-dimensional Array en fichier PNG
    (Array_2N, str, dict ) -> NoneType

    """

    pngWriter = png.Writer(width=info["size"][0], height=info["size"][1], 
        greyscale= info["greyscale"], planes=info["planes"],  
        alpha=info["alpha"], interlace= info["interlace"])

    pngWriter.write(open(path, "wb"), png_2d)


def compound_byte(high, low):
    """
    docstring
    Fonction qui permet de combiner 2 octets l'un de poids fort et l'autre de poids faible
    (uint8, uint8) -> uint16

    >>> compound_byte(2, 2)
    514
    >>> compound_byte(10, 145)
    2705
    >>> compound_byte(100, 145)
    25745
    >>>
    """
    return 256*high + low

def shape_2D(array_2D):
    """
    docstring
    FOnction qui permet de retrouver le shape d'un tableau à deux dimensions
    (list(list)) -> tuple
    >>> a = [
    ...         [1], [2]
    ...     ]
    >>> shape_2D(a)
    (2, 1)
    >>> a = [
    ...         [1,3], [2,4], [3, 4]
    ...     ]
    >>> shape_2D(a)
    (3, 2)
    >>> a = [
    ...         [1,3, 2, 3], [2,4,3, 4]
    ...     ]
    >>> shape_2D(a)
    (2, 4)
    >>>
    """
    return (len(array_2D), len(array_2D[0]))

def set_value_2D(array_2D, index, value):
    """
    docstring
    Fonction qui permet de parcourir la matrice et de modifier l'element correspondant à l'index
    (list(list), tuple, number) -> NoneType
    >>> a
    [[1, 3, 2, 3], [2, 4, 3, 4]]
    >>> set_value_2D(a, (0, 0), 0)
    >>> a
    [[0, 3, 2, 3], [2, 4, 3, 4]]
    >>> set_value_2D(a, (0, 3), 0)
    >>> a
    [[0, 3, 2, 0], [2, 4, 3, 4]]
    >>> set_value_2D(a, (1, 1), 1)
    >>> a
    [[0, 3, 2, 0], [2, 1, 3, 4]]
    >>> 
    """
    array_2D[index[0]][index[1]] = value

def get_index_2D(array_2D, index):
    """
    docstring
    Fonction qui permet de parcourir la matrice et de retourner l'element correspondant à l'index
    (list(list), tuple) -> number
    >>> a
    [[1, 3, 2, 3], [2, 4, 3, 4]]
    >>> get_index_2D(a, (0, 0)
    ... )
    1
    >>> get_index_2D(a, (0, 2)
    ... )
    2
    >>> get_index_2D(a, (1, 3))
    4
    >>> 
    """
    if index[0]>=len(array_2D) or index[1]>=len(array_2D[0] ):
        raise Exception("Index Incorrect")
    return array_2D[index[0]][index[1]]

def find(png_2d):
    """
    docstring
    Fonction qui permet  de trouver un message caché dans un fichier PNG
    on parcours les elements du array avec un deplacement de OFFSET pour récuperer les caractères 
    (file) -> str
    """
    index=(0,0)
    msg = ""
    while END_OF_MESSAGE not in msg:
        low = get_index_2D(png_2d, index)
        index, end = next_index(shape=shape_2D(png_2d), current_index = index)
        #lors qu'on finie de lire tous les pixels
        if end : 
            raise Exception("Aucun message trouvé dans le fichier")

        high = get_index_2D(png_2d, index)

        msg+=chr(compound_byte(high = high, low = low))

        index, end = next_index(shape=shape_2D(png_2d), current_index = index)
        
        #lors qu'on finie de lire tous les pixels
        if end : 
            raise Exception("Aucun message trouvé dans le fichier")
        
    return msg

def format(msg):
    """
    docstring

    Fonction qui permet de formater le message trouvé dans le fichier PNG
    Elle enlève le message de FIN
    On l'affiche à l'aide de strings de Unix et retourne la chaine de caractère

    (str) -> str

    >>> format("alassane#FIN#")
    'alassane'
    >>> format("alassane #FIN#")
    'alassane '
    >>> format("alassane Mariko    ")
    'alassane Mariko    '
    >>> 
    """
    inter = ""
    if END_OF_MESSAGE in msg:
        for i in range(len(msg)-len(END_OF_MESSAGE)):
           inter+=msg[i]
    else:
        inter = msg


    p = subprocess.run(['strings'], stdout = subprocess.PIPE,
            input=inter, encoding='utf-8')
    return p.stdout

def hide(png_2d, msg):
    """
    docstring
    Fonction qui permet de cacher dans un fichier PNG un message 
    (file, str) -> NoneType

    """
    msg+=END_OF_MESSAGE
    index = (0,0)
    for x in msg : 
        set_value_2D(png_2d, index, low_byte(ord(x)))  
        index, _ = next_index(shape = shape_2D(png_2d), current_index = index)
        set_value_2D(png_2d, index, high_byte(ord(x)))
        index, _ = next_index(shape = shape_2D(png_2d), current_index = index)
    return png_2d


def low_byte(number):
    """
    docstring
    FOnction qui permet de retourner en decimale la valeur de l'octet  de poids faible
    (int)-> uint8
    >>> low_byte(8)
    8
    >>> low_byte(256)
    0
    >>> low_byte(1000)
    232
    >>> 

    """
    return number%256

def high_byte(number):
    """
    docstring
    FOnction qui permet de retourner en decimale la valeur de l'octet  de poids fort
    number doit être comprise entre [0, 65535]
    (uint16)-> uint8
    >>> high_byte(8)
    0
    >>> high_byte(256)
    1
    >>> high_byte(1000)
    3

    """
    return int((number%65536)/256)

def next_index(shape, current_index):
    """
    docstring
    Fonction qui permet de retourner le prochain index après un saut de 5 pixel
    (tuple, tuple) -> tuple

    >>> next_index((100,100), (0,0))
    (0, 5)
    >>> next_index((100,35), (2,5))
    (2, 10)
    >>> next_index((100,35), (3,30))
    (4, 0)

    """
    current_index_list = list(current_index)
    shape_list = list(shape)
    current_index_list[1]+=OFFSET
    end = False
    if current_index_list[1]>=shape_list[1]:
        current_index_list[1]%=shape_list[1]
        current_index_list[0] += 1
    if current_index_list[0] == shape_list[0]: 
        end = True


    return tuple(current_index_list), end

def get_png_file(path):
    """
    docstring 
    Fonction qui permet de lire un  fichier PNG et verifier que c'est bien un fichier ou génère une erreur
    elle retourne le array en 2D et le dictionnaire info
    (str)->Array-2D, dict

    >>> get_png_file("img/img.png")
    (array([[108,  29,  29, ...,  29,  29, 255],
        [ 29,  29,  29, ...,  29,  29, 255],
        [ 29,  29,  29, ...,  29,  29, 255],
        ...,
        [ 31,  20,  29, ..., 125, 199, 255],
        [ 31,  20,  30, ..., 125, 199, 255],
        [ 31,  20,  29, ..., 125, 199, 255]], dtype=uint8), {'greyscale': False, 'alpha': True, 'planes': 4, 'bitdepth': 8, 'interlace': 0, 'size': (1600, 900)})
    >>> get_png_file("img/3.png")
    (array([[ 30,  30,  30, ..., 207, 200, 255],
        [ 30,  30,  30, ..., 188, 143, 255],
        [ 30,  30,  30, ..., 164, 111, 255],
        ...,
        [ 89,  87,  46, ...,  30,  30, 255],
        [ 80, 138,  86, ...,  30,  30, 255],
        [ 30,  30,  30, ...,  30,  30, 255]], dtype=uint8), {'greyscale': False, 'alpha': True, 'planes': 4, 'bitdepth': 8, 'interlace': 0, 'size': (51, 27)})
    >>> get_png_file("img/test.txt")
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "<stdin>", line 11, in get_png_file
    File "/home/alasco/.local/lib/python3.8/site-packages/png.py", line 1813, in read
        self.preamble(lenient=lenient)
    File "/home/alasco/.local/lib/python3.8/site-packages/png.py", line 1609, in preamble
        self.validate_signature()
    File "/home/alasco/.local/lib/python3.8/site-packages/png.py", line 1595, in validate_signature
        raise FormatError("PNG file has invalid signature.")
    png.FormatError: FormatError: PNG file has invalid signature.
    >>> 
    """
    reader = png.Reader(filename= path)
    png_tuple = reader.read()
    # on met le tableau en array
    png_2d = []
    for x in iter(png_tuple[2]):
        png_2d.append(x)
    #print("Shape : ( {}, {} ) info : {}".format( len(png_2d), len(png_2d[0]), png_tuple[3]))
    
    return png_2d, png_tuple[3]