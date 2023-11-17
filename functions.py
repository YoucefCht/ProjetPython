import os


def president_name(directory,
                   extension):  # fonctions pour sortir les documents d'un fichier et donner une liste des présidents présents
    files_names = set()
    for files in os.listdir(directory):  # lit les fichiers contenue dans la variable (directory)
        if files.endswith(extension):  # seulement si le fichier est de type de la variable extension (.txt.py ...)
            character_to_remove = ["Nomination_", ".txt", "1", "2"]  # enlève les caractères gênants
            for value in character_to_remove:
                files = files.replace(value, "")

            files_names.add(files)
    return list(files_names)


def copy(directory, extension, cleaned_folder):
    for files in os.listdir(directory):
        if files.endswith(extension):
            input_path = os.path.join(directory, files)
            output_path = os.path.join(cleaned_folder, files.lower())  # replace 'filename' with 'files'
            with open(input_path, "r") as f, open(output_path, "w") as cleaned:
                contenue = f.read()
                for value in contenue:
                    if 65 <= ord(value) <= 90:
                        value = chr(ord(value) + 32)
                        cleaned.write(value)
                    else:
                        cleaned.write(value)


def punctuation(chemin):
    ponct = [',', '.', ';', ':', '!', '?', '(', ')', '[', ']', '{', '}', '<', '>', '/', '\\', '|', '@', '#', '$', '%',
             '^', '&', '*', '_', '+', '=', '`', '~', '"']
    ponct2 = ["'", "-"]

    for filename in os.listdir(chemin):
        if filename.endswith(".txt"):
            file_path = os.path.join(chemin, filename)

            with open(file_path, "r") as file:
                content = file.read()

            for value in ponct:
                content = content.replace(value, "")

            for value in ponct2:
                content = content.replace(value, " ")

            with open(file_path, "w") as file:
                file.write(content)