from functions import *
#import the functions from functions.py

chemin_acces = 'speeches'
extension = '.txt'
cleaned_folder = 'cleaned'

copy = copy(chemin_acces, extension, cleaned_folder)
list = president_name(chemin_acces, extension)
lien = 'cleaned'
function_tf(lien)
function_idf(lien)
Matrix(lien)
punctuation(lien)
matrix = Matrix(lien)
useless_words(matrix)

print('''
      ####   #####  ####   ####   ###        ####  #   #   ###  ###### ####    ###  ######
      #      #      #   #  #       #        #      #   #  #   #   ##   #   #  #   #   ##
      ####   ####   ####   ###     #        #      #####  #####   ##   ####   #   #   ##
      #      #      #  #   #       #        #      #   #  #   #   ##   #   #  #   #   ##
      ####   #      #   #  ####   ###        ####  #   #  #   #   ##   ####    ###    ##
''')
print("Hello, Choose your action : \n \n 1- Display the list of least important words \n 2- Display the word(s) with the highest TD-IDF score \n 3- Display the most repeated word(s) by President Chirac \n 4- Display the president(s) who said the word Nation and who repeated it the most times. \n 5- Display the first president to talk about climate or ecology \n 6- Display the words that all the president mention. \n 7- Ask a question to the ChatBot  \n 8- End the discussion" )



matrix=Matrix('cleaned')
while True:
  number=int(input("What is your choice ? \n")) 
  #The user choose an integer that correspond to the question between 1 and 7
  
  if number==1:
    print("The list of least important words is : \n")
    print((useless_words(matrix)))
  #Print the first question
  
  elif number==2:
    print("The word(s) with the highest TD-IDF score is : \n")
    strong_words(matrix)
  #Print the second question
  
  elif number==3:
    print("The most repeated word(s) by President Chirac is : \n")
    print(lot_words_chirac(lien))
  #Print the third question
  
  elif number==4:
    print("The president(s) who said the word Nation and who repeated it the most times are : \n")
    nation(lien)
  #Print the fourth question
  
  elif number==5:
    print("The first president to talk about climate or ecology is : \n")
    climat()
  #Print the fifth question
  
  elif number==6:
    print("The words that all the president mention are : \n")
    common_words_all_presidents()
  #Print the sixth question
  
  elif number == 7 :
    Question = input("Ask your question :")
    search(lien, Question)
    most_relevant_doc(Question)
  #print the seven question 

  elif number==8:
    print("End of discussion")
    break
  #Fin de la discussion

  else:
    print("Please enter a number between 1 and 7 \n")
  #Print an error message if tnumber entered is not between 1 and 7

  
