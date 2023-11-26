from functions import *

#Chemin accès 
chemin_acces = 'speeches'
extension = '.txt'
cleaned_folder = 'cleaned'

copy = copy(chemin_acces, extension, cleaned_folder)
list = president_name(chemin_acces, extension)

print("List of the names of all the president presents in the folder speeches :", list)

#Chemin accès pour la fonction "punctuation"



#calcul tf-idf
lien = 'cleaned'
Matrix(lien)
punctuation(lien)

#Question 1 et 2

matrix = Matrix(lien)
useless_words(matrix)
strong_words(matrix)

'''Question 3
As we can see in the file "Most_Common_Chirac_Words.txt"
His most common words are :
de: 97
la: 64
l: 48
et: 46
les: 38
le: 36
à: 32
d: 29
une: 28
des: 22
'''
lot_words_chirac()


#print(least_important_words(Matrix))

'''Question 4:
As we can see in the file "Most_Mentions_of_Nation.txt" the president who said the word "nation" are :

'''


nation()

#Question 5 

climat()

#Question 6 
common_words_all_presidents()
