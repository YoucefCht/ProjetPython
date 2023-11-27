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
    # function that do the tf calculation
    for filename in os.listdir(lien):
        if filename.endswith(".txt"):
            file_path = os.path.join(lien, filename)

            with open(file_path, 'r') as f1, open('Dictionnary/Dico_TF_' + filename, 'w') as f2:
                content = f1.read()

                word_count = {}
                words = content.split()  # split the contentt in a list of words

                for word in words:
                    if word not in word_count:
                        word_count[word] = 1
                    else:
                        word_count[word] += 1

                for word, count in word_count.items():
                    f2.write(f"{word}: {count}\n")
                # count the times a number apear


def count(directory):
    w_d_count = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)

            with open(file_path, 'r') as file:
                content = file.read()
                words = set(content.split())

                for word in words:
                    if word not in w_d_count:
                        w_d_count[word] = 1
                    else:
                        w_d_count[word] += 1
    return w_d_count
    # count the times a number apear


def function_idf(directory, output_file='idf_scores.txt'):
    # function that do the calcullation of idf
    total_documents = len(os.listdir(directory))
    w_d_count = {}

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)

            with open(file_path, 'r') as file:
                content = file.read()
                words = set(content.split())
                for word in words:
                    w_d_count[word] = w_d_count.get(word, 0) + 1

    # make the calcul IDF for each words
    idf_scores = {}
    for word, count in w_d_count.items():
        idf_scores[word] = math.log10(total_documents / count) if count != 0 else 0

    # write the dictionnary in a txt file
    with open(output_file, 'w') as file:
        for word, score in idf_scores.items():
            file.write(f"{word}: {score}\n")

    return idf_scores


def Matrix(directory, output_file='tf_idf.txt'):
    total_documents = len(os.listdir(directory))
    IDF = function_idf(directory)
    tf_idf_matrix = {}
    # récolte de tout les mots
    all_words = set()
    words_in_files = {file: set() for file in os.listdir(directory)}

    for file in os.listdir(directory):
        with open(os.path.join(directory, file), 'r', encoding='utf-8') as file_content:
            words = set(file_content.read().split())
            all_words.update(words)
            words_in_files[file] = words
    # annonce the matrice
    for word in all_words:
        tf_idf_matrix[word] = [0] * total_documents
    for file_idx, file in enumerate(os.listdir(directory)):
        words_in_file = words_in_files[file]
        for word in words_in_file:
            tfidf = float(IDF.get(word, 0))
            tf_idf_matrix[word][file_idx] = tfidf
    # matrice tf-idf in a txt
    with open(output_file, 'w') as file:
        for word, tfidf_scores in tf_idf_matrix.items():
            scores_str = ' '.join(map(str, tfidf_scores))
            if any(tfidf_scores):
                file.write(f"{word}: {scores_str}\n")

    return tf_idf_matrix


# return matrix tf-idf
def useless_words(tf_idf_matrix, output_file='useless.txt'):
    useless_words = []

    for word, tf_idf_scores in tf_idf_matrix.items():
        total_score = sum(tf_idf_scores)
        if total_score == 0:
            useless_words.append(word)

    with open(output_file, 'w') as file:
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




















