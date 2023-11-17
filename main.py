from functions import *


#Chemin accès pour les fonctions "president_name" et "copy"
chemin_acces = 'speeches'
extension = '.txt'
cleaned_folder = 'cleaned'

copy = copy(chemin_acces, extension, cleaned_folder)
list = president_name(chemin_acces, extension)

print("List of the names of all the president presents in the folder speeches :", list)

#Chemin accès pour la fonction "punctuation"
chemin_accès = punctuation('cleaned')
print(chemin_accès)

#Occurence number
chemin_acc = 'Dictionnary'
occurence = occurence(chemin_acc)