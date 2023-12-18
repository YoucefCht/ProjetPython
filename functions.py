from math import *
import math
import os


def president_name(directory, extension):
    # functions to output documents from a file and provide a list of presidents

    files_names = set()
    # set to store the names of the presidents

    for files in os.listdir(directory):
        # reads the files contained in the variable directory

        if files.endswith(extension):
            # only if file is from the variable extension (.txt.py ...)

            character_to_remove = ["Nomination_", ".txt", "1", "2"]
            # List of annoying features to remove

            for value in character_to_remove:
                files = files.replace(value, "")
            # removes annoying characters

            files_names.add(files)
            # add the name of the president to the set

    return list(files_names)
    # return the list of presidents


def copy(directory, extension, cleaned_folder):
    # function that copies files to a folder taking three parameters :
    # directory (which contains the files to be copied),
    # extension (which specifies the file type to be copied)
    # cleaned_folder (which is the destination folder where the files will be copied)

    for files in os.listdir(directory):
        if files.endswith(extension):
            input_path = os.path.join(directory, files)
            # 
            output_path = os.path.join(cleaned_folder, files.lower())
            # replace 'filename' with 'files'

            with open(input_path, "r") as f, open(output_path, "w") as cleaned:
                contenue = f.read()
                for value in contenue:
                    if 65 <= ord(value) <= 90:
                        value = chr(ord(value) + 32)
                        cleaned.write(value)
                    # For each letter in "contenue" transforms uppercase into lowercase
                    else:
                        cleaned.write(value)


def punctuation(chemin):
    # fonction qui supprime tout les caractères spéciaux de

    ponct = [',', '.', ';', ':', '!', '?', '(', ')', '[', ']', '{', '}', '<', '>', '/', '\\', '|', '@', '#', '$', '%',
             '^', '&', '*', '_', '+', '=', '`', '~', '"']
    # List of special characters to be deleted
    ponct2 = ["'", "-", chr(10)]
    # List of special characters to be replaced by a space

    for filename in os.listdir(chemin):
        if filename.endswith(".txt"):
            file_path = os.path.join(chemin, filename)

            with open(file_path, "r") as file:
                content = file.read()

            for value in ponct:
                content = content.replace(value, "")
            # supprime les caractères spéciaux de la première list

            for value in ponct2:
                content = content.replace(value, " ")
            # remplace les caractères spéciaux de la deuxième liste par des espaces
            file_path = os.path.join(chemin, filename)

            with open(file_path, "w") as file:
                file.write(content)


def function_tf(lien):
    word_TF = {}
    key_words = set()

    # Collecte de tous les mots uniques dans tous les documents
    for filename in os.listdir(lien):
        if filename.endswith(".txt"):
            file_path = os.path.join(lien, filename)

            with open(file_path, 'r') as f1:
                content = f1.read()
                words = set(content.split())
                key_words.update(words)

    # Initialisation des listes avec des zéros pour chaque mot dans le dictionnaire
    for word in key_words:
        word_TF[word] = [0] * 8  # 8 documents au total, initialisation à zéro

    # Calcul du TF pour chaque mot dans chaque document
    for index, filename in enumerate(os.listdir(lien)):
        if filename.endswith(".txt"):

            file_path = os.path.join(lien, filename)

            with open(file_path, 'r') as f1, open('Dictionnary/Dico_TF_' + filename, 'w') as f2:

                content = f1.read()
                words = content.split()

                # Mise à jour du TF pour chaque mot dans le document actuel
                for word in words:
                    if word in word_TF:
                        word_TF[word][index] += 1

                for word, value in word_TF.items():
                    f2.write(f"{word} : {value}\n")

    return word_TF


def count(directory):
    word_count = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)

            with open(file_path, 'r') as file:
                content = file.read()
                words = set(content.split())

                for word in words:
                    if word not in word_count:
                        word_count[word] = 1
                    else:
                        word_count[word] += 1
    return word_count
    # count the times a number apear


def function_idf(directory, output_file="idf_scores.txt"):
    total_doc = len(os.listdir(directory))
    TF = function_tf(directory)
    word_in_doc = {}
    idf_scores = {}

    for word in TF.keys():
        word_in_doc[word] = 0
        for doc in os.listdir(directory):
            if word in open(os.path.join(directory, doc)).read():
                word_in_doc[word] += 1

    for word, count in word_in_doc.items():
        idf_scores[word] = math.log10(total_doc / count)

    with open(output_file, 'w') as f1:
        for word, score in idf_scores.items():
            f1.write(f"{word}: {score}\n")

    return idf_scores


def Matrix(directory):
    TF = function_tf(directory)
    IDF = function_idf(directory)
    tf_idf_matrix = {}

    for word, idf in IDF.items():
        for wordd, tf in TF.items():
            if word == wordd:
                tf_idf_matrix[word] = []
                for i in range(len(tf)):
                    tf_idf_matrix[word].append(idf * tf[i])

    with open("tf_idf.txt", 'w') as f1:
        for word, tf_idf in tf_idf_matrix.items():
            f1.write(f"{word} : {tf_idf}\n")

    return tf_idf_matrix


def useless_words(tf_idf_matrix, output_file='useless.txt'):
    useless_words = []

    for word, tf_idf_scores in tf_idf_matrix.items():
        total_score = sum(tf_idf_scores)
        if total_score == 0:
            # Vérification des caractères spéciaux dans le mot
            cleaned_word = ''.join(c for c in word if c.isprintable())
            # Si le mot nettoyé est vide, on le remplace par '[UNKNOWN]'
            if not cleaned_word:
                cleaned_word = '[UNKNOWN]'
            useless_words.append(cleaned_word)

    with open(output_file, 'w', encoding='utf-8') as file:
        for word in useless_words:
            file.write(f"{word}\n")
    return useless_words


def strong_words(tf_idf_matrix, output_file='strong word.txt'):
    strong_words = {}

    for word, tf_idf_scores in tf_idf_matrix.items():
        max_score = max(tf_idf_scores)
        if max_score > 0:
            strong_words[word] = max_score

    sorted_words = sorted(strong_words.items(), key=lambda x: x[1], reverse=True)

    with open(output_file, 'w') as file:
        for word, score in sorted_words:
            file.write(f"{word}: {score}\n")
    temp = []
    for i in range(10):
        temp.append(sorted_words[i])
    return print(', '.join((f'{i}, {j}' for i, j in temp)))


def lot_words_chirac():
    chirac_files = ["Dictionnary/Dico_TF_nomination_chirac1.txt", "Dictionnary/Dico_TF_nomination_chirac2.txt"]
    chirac_words = {}

    # merge the files
    for file_path in chirac_files:
        with open(file_path, 'r') as file:
            for line in file:
                word, count = line.split(": ")
                chirac_words[word] = chirac_words.get(word, 0) + int(count)

    # sort words by frequency
    sorted_words = sorted(chirac_words.items(), key=lambda x: x[1], reverse=True)

    # choose the 10 more frequent word
    top_words = sorted_words[:10]

    # write the most common words
    with open("Most_Common_Chirac_Words.txt", 'w') as output_file:
        for word, count in top_words:
            output_file.write(f"{word}: {count}\n")

    return print(', '.join((f'{i}, {j}' for i, j in top_words)))


def nation():
    presidents = {
        "Chirac": ["Dictionnary/Dico_TF_nomination_chirac1.txt", "Dictionnary/Dico_TF_nomination_chirac2.txt"],
        "Giscard d'Estaing": ["Dictionnary/Dico_TF_nomination_giscard destaing.txt"],
        "Hollande": ["Dictionnary/Dico_TF_nomination_hollande.txt"],
        "Macron": ["Dictionnary/Dico_TF_nomination_macron.txt"],
        "Mitterrand": ["Dictionnary/Dico_TF_nomination_mitterrand1.txt",
                       "Dictionnary/Dico_TF_nomination_mitterrand2.txt"],
        "Sarkozy": ["Dictionnary/Dico_TF_nomination_sarkozy.txt"]
    }

    word_count = {}
    for president, files in presidents.items():
        word_count[president] = 0
        for file_path in files:
            with open(file_path, 'r') as file:
                for line in file:
                    word, count = line.split(": ")
                    if word.lower() == 'nation':
                        word_count[president] += int(count)

    # sort the president by the number of "nation" used
    sorted_presidents = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

    # write the result in a file
    with open('Most_Mentions_of_Nation.txt', 'w') as output_file:
        output_file.write("Président(s) et mentions du mot 'Nation':\n")
        for president, mentions in sorted_presidents:
            output_file.write(f"{president}: {mentions} mentions\n")
    return print("The president that said the word nation are : \n",
                 ("\n".join((f'{i} {j}' for i, j in sorted_presidents))), "\n with",
                 (', '.join(map(str, sorted_presidents[0]))), "who said it the most")
    # return the sentence with the value that we get


def climat():
    presidents = {
        "Chirac": ["Dictionnary/Dico_TF_nomination_chirac1.txt", "Dictionnary/Dico_TF_nomination_chirac2.txt"],
        "Giscard d'Estaing": ["Dictionnary/Dico_TF_nomination_giscard destaing.txt"],
        "Hollande": ["Dictionnary/Dico_TF_nomination_hollande.txt"],
        "Macron": ["Dictionnary/Dico_TF_nomination_macron.txt"],
        "Mitterrand": ["Dictionnary/Dico_TF_nomination_mitterrand1.txt",
                       "Dictionnary/Dico_TF_nomination_mitterrand2.txt"],
        "Sarkozy": ["Dictionnary/Dico_TF_nomination_sarkozy.txt"]
    }

    first_mention = {}
    for president, files in presidents.items():
        first_mention[president] = float('inf')
        for file_path in files:
            with open(file_path, 'r') as file:
                for line in file:
                    word, _ = line.split(": ")
                    if word.lower() in ['climat', 'écologie']:
                        current_mention = files.index(file_path) + 1
                        if current_mention < first_mention[president]:
                            first_mention[president] = current_mention

    # look for the president that said the word the most times
    first_president_mention = min(first_mention, key=first_mention.get)

    with open('First_Mention_Climate_Ecology.txt', 'w') as output_file:
        output_file.write(f"Le premier président à mentionner 'climat' ou 'écologie' est {first_president_mention}.\n")
    return print(first_president_mention, "\n")


def common_words_all_presidents():
    presidents = {
        "Chirac": ["Dictionnary/Dico_TF_nomination_chirac1.txt", "Dictionnary/Dico_TF_nomination_chirac2.txt"],
        "Giscard d'Estaing": ["Dictionnary/Dico_TF_nomination_giscard destaing.txt"],
        "Hollande": ["Dictionnary/Dico_TF_nomination_hollande.txt"],
        "Macron": ["Dictionnary/Dico_TF_nomination_macron.txt"],
        "Mitterrand": ["Dictionnary/Dico_TF_nomination_mitterrand1.txt",
                       "Dictionnary/Dico_TF_nomination_mitterrand2.txt"],
        "Sarkozy": ["Dictionnary/Dico_TF_nomination_sarkozy.txt"]
    }

    # keep the words of each president
    words_per_president = {president: set() for president in presidents}

    # read the dictionnary for each president
    for president, files in presidents.items():
        for file_path in files:
            with open(file_path, 'r') as file:
                for line in file:
                    word, _ = line.split(": ")
                    words_per_president[president].add(word)
    common_words = set.intersection(*words_per_president.values())

    # write the words in a file
    with open('Common_Words_All_Presidents.txt', 'w') as output_file:
        output_file.write("Mots communs à tous les présidents :\n")
        for word in common_words:
            output_file.write(f"{word}\n")
    return print("The non really important words said by every president are : \n", common_words)


# Chat_bot projet PART II

# 1. Question tokenization
def list_question(question):
    question = question.lower()
    list = question.split()

    return list


# 2. Search for the question words in the Corpus
def search(directory, question):
    L = []
    list_result = list_question(question)

    for files in os.listdir(directory):
        if files.endswith(".txt"):
            file = os.path.join(directory, files)

            with open(file, "r") as f1:
                content = f1.read()
                words = content.split()

                for value in words:
                    for val in list_result:
                        if value == val:
                            L.append(val)

    return list(set(L))


# 3. Calculate the TF-IDF vector for the terms in question
def vector(question):
    idf_dico = function_idf('cleaned')
    list_result = list_question(question)
    list_common = search('cleaned', question)

    dico_tf = {}
    tf_idf_question = {}
    # count = len(list_result)

    for value in list_result:
        if value in dico_tf:
            dico_tf[value] += 1
        else:
            dico_tf[value] = 1

    for value in list_result:
        if value not in list_common:
            dico_tf[value] = 0
    """
    for word, value in dico_tf.items():
        dico_tf[word] = value / count
    """
    for word, value in dico_tf.items():
        if word in idf_dico:
            tf_idf_question[word] = dico_tf[word] * idf_dico[word]
        else:
            tf_idf_question[word] = dico_tf[word]

    return tf_idf_question


# 4. Calculating similarity

# a. The scalar product
def scalar_product(question):
    vectorA = vector(question)
    matrix = Matrix('cleaned')
    vectorB = {}
    scalar = {}

    for i in range(0, 8):
        vector_bis = {}
        for word, tf_idf in matrix.items():
            if word in vectorA:
                vector_bis[word] = tf_idf[i]
        vectorB['Doc_' + str(i + 1)] = vector_bis

    vectorB_bis = vectorB.copy()  # no modification for vectorB_bis if vectorB will be modified

    for document, vectorr in vectorB.items():
        for word, tf_idf in vectorr.items():
            scalar[word] = vectorr[word] * vectorA[word]
        vectorB[document] = sum(scalar.values())

    """
    maximum = max(vectorB.values())
    for document, value in vectorB.items():
        if value == maximum:
            print("Document with maximum scalar product:", document)
            break
    """

    return vectorB_bis, vectorB


# b. The norm of a vector
def norm_vector(question):
    vectorB, scalar = scalar_product(question)
    vectorA = vector(question)
    norm_A = 0  # norm of the question
    norm_B = {}

    for word, value in vectorA.items():
        norm_A += value ** 2
    norm_A = sqrt(norm_A)

    for doc, dico in vectorB.items():
        norm_bis = 0
        for value in dico.values():
            norm_bis += value ** 2

        norm_B['norm_' + doc] = sqrt(norm_bis)

    return norm_A, norm_B


# c. Calculating similarity
def similarity(question):
    vectorB, scalar_AB = scalar_product(question)
    normA, normB = norm_vector(question)
    similarity = {}

    for i in range(len(scalar_AB)):

        if normA != 0 and (list(normB.values())[i]) != 0:
            similarity['Similarity_Doc_' + str(i + 1)] = list(scalar_AB.values())[i] / (
                        normA * (list(normB.values())[i]))
        else:
            similarity['Similarity_Doc_' + str(i + 1)] = 0

    return similarity


# 5. Calculating the most relevant document ; 6. Generating a response
def most_relevant_doc(question):
    similarity_dico = similarity(question)
    liste_files = os.listdir('speeches')
    vector_question = vector(question)

    print(f"Question : {question}")

    for index, (word, value) in enumerate(similarity_dico.items()):
        if value == max(similarity_dico.values()):
            # print(f'Relevant document returned : {word}')
            doc = liste_files[index]
            print(f"Relevant document returned : {doc}")
            break

    for word, value in vector_question.items():
        if value == max(vector_question.values()):
            first_occurence = word
            print(f"Word with the highest TF-IDF : {word} ")

    # 7. Refine an answer
    with open(f"speeches/{doc}", 'r') as f1:
        content = f1.read().lower()
        sentences = content.split('.')

        question_user = question.split()

        for sentence in sentences:
            if first_occurence in sentence:
                if question_user[0] == "Comment":
                    answer = 'Après analyse, ' + sentence.strip() + '.'  # erase space at the beginning and the end of the sentence

                elif question_user[0] == "Pourquoi":
                    answer = 'Car, ' + sentence.strip() + '.'

                elif question_user[0] == "Peux-tu":
                    answer = 'Oui, bien sûr ! ' + sentence.strip() + '.'

                else:
                    answer = sentence.strip().capitalize() + '.'  # .capitalize (put the first letter in capital letter)

                print(f"The response generated: {answer}")
                break

