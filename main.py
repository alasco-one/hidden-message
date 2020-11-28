import argparse
import utilities


parser = argparse.ArgumentParser()

#On ajoute le cas path pour spécifier le chémin vers fichier PNG
parser.add_argument("path", help="specifies the path to PNG file", type=str)

#On ajoute le cas -w pour choisir le mode wrintting
parser.add_argument("-w", "--writting", help="chooses a writting mode",action="store_true")

#On ajoute le cas -f pour definir le chemin du fichier utiliser.
parser.add_argument("-f", "--file", help="specifies a file name",type=str)

#On ajoute le cas -t pour definir le texte à  utiliser.
parser.add_argument("-t", "--text", help="specifies a text",type=str)

#variable contenant le message à cacher
msg=""

args = parser.parse_args()

png, info=utilities.get_png_file(args.path)

if args.writting : 
    # On choisie le mode writting
    if args.file:
        # Dans ce cas ci le file name a été defini
        # On doit donc utiliser le contenu du fichier "file"
        print("File specified : {}".format(args.file))
        f = open(args.file,'r')
        msg=f.read()

    elif args.text:
        # Dans ce cas ci le file name a été defini
        # On doit donc utiliser le contenu du fichier "file"
        print("Text specified : {}".format(args.text))
        msg = args.text
    else:
        msg = input("Enter un message to hide : ")

    #print( "Voici votre message :  {}".format(msg))
    utilities.check(png, msg)

    utilities.save_to_png(utilities.hide(png, msg), args.path, info)
    print( "Message caché avec succès !")


else:
    # On choisit donc le mode reading
    #print("Find  :  {}".format(png.shape))
    print("{}".format(utilities.format(utilities.find(png))))
