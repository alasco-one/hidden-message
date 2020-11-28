
import png
import numpy

#Le symbole de la fin du message 
END_OF_MESSAGE = "#FIN#"
# le decalage de pixel lors du hidding et du finding pour le 'effet ne soit pas si visible
OFFSET = 600

def check(png_2d, msg):
    """
    docstring
    Fonction qui permet de verifier qu'un message peut être caché dans un image

    (Array_2D, str) raise Exception -> NoneType
    """
    if (png_2d.size/OFFSET) <= (len(msg) + len(END_OF_MESSAGE))*2 :
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
        low = png_2d[index]
        index, end = next_index(shape=png_2d.shape, current_index = index)
        #lors qu'on finie de lire tous les pixels
        if end : break

        high = png_2d[index]

        msg+=chr(compound_byte(high = high, low = low))

        index, end = next_index(shape=png_2d.shape, current_index = index)
        
        #lors qu'on finie de lire tous les pixels
        if end : break



        
    return msg

def format(msg):
    """
    docstring

    Fonction qui permet de formater le message trouvé dans le fichier PNG
    Elle enlève le message de FIN

    (str) -> str

    >>> format("alassane#FIN#")
    'alassane'
    >>> format("alassane #FIN#")
    'alassane '
    >>> format("alassane Mariko    ")
    'alassane Mariko    '
    >>> 
    """
    if END_OF_MESSAGE in msg:
        inter = ""
        for i in range(len(msg)-len(END_OF_MESSAGE)):
           inter+=msg[i]
        return inter 
    else:
        return msg

def hide(png_2d, msg):
    """
    docstring
    Fonction qui permet de cacher dans un fichier PNG un message 
    (file, str) -> NoneType

    """
    msg+=END_OF_MESSAGE
    index = (0,0)
    for x in msg : 
        png_2d[index] = low_byte(ord(x))
        index, _ = next_index(shape = png_2d.shape, current_index = index)
        png_2d[index] = high_byte(ord(x))
        index, _ = next_index(shape = png_2d.shape, current_index = index)
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
    
    return numpy.array(png_2d), png_tuple[3]