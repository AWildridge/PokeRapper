import difflib
from google_images_download import google_images_download
import os

"""
Find the words to filter out from finding the differences between search_word and words in similar_words
param: search_word word that is being searched
param: similar_words words that are similar to search_word and need to be filtered out
"""
def find_filter_words(search_word, similar_words):
    filter_words = ''
    for similar_word in similar_words:
        print(similar_word)
        if similar_word == search_word:
            continue
        processed_search_word = search_word.replace(' ', '\n') + '\n'
        processed_similar_word = similar_word.replace(' ', '\n') + '\n'
        diff = difflib.ndiff(processed_search_word.splitlines(1), processed_similar_word.splitlines(1))
        diff_list = ''.join(diff).split('\n')
        print(diff_list)
        for word in diff_list:
            if word == '':
                continue
            if word[0] == '+':
                word = word.split()[1]
                if ' ' in word:
                    print("Blank space in word!")
                filter_words += ' -' + word
    return filter_words

data_dir = "/home/aj/PokeRap/Pokemon"
pokemon_list = os.listdir(data_dir)

response = google_images_download.googleimagesdownload()
for pokemon in pokemon_list:
    if pokemon == 'data':
        continue
    arguments = {}
    alternate_forms = os.listdir(data_dir + "/" + pokemon)
    if len(alternate_forms) > 0:
        print("Processing for alternate forms: " + str(alternate_forms))
        for alternate_form in alternate_forms:
            # need to filter out the other alternate forms in search
            filter_words = find_filter_words(alternate_form, alternate_forms)
            arguments["keywords"] = "\"" + alternate_form + "\"" + filter_words + " -shiny"
            print("The keywords for pokemon " + str(alternate_form) + " is " + str(arguments["keywords"]))
            arguments["limit"] = 100
            arguments["output_directory"] = "/home/aj/PokeRap/Pokemon/"
            arguments["image_directory"] = pokemon + "/" + alternate_form
            response.download(arguments)
            print("Downloaded images for pokemon: " + alternate_form)
        # now download for regular pokemon
        # need to filter alternates from pokemon...this may not be true for all pokemon
        only_has_alternate_forms = ["Zygarde", "Deoxys", "Giratina", "Shaymin", "Tornadus", "Thundurus", "Landorus", "Keldeo", "Meloetta", "Aegislash", "Wormadam", "Darmanitan", "Pumpkaboo", "Gourgeist", "Hoopa", "Meowstic"]
        if pokemon in only_has_alternate_forms:
            continue
        filter_words = find_filter_words(pokemon, alternate_forms)
        arguments["keywords"] = "\"" + pokemon + "\"" + filter_words + " -shiny"
        print("The keywords for pokemon " + str(pokemon) + " is " + str(arguments["keywords"]))
        arguments["limit"] = 100
        arguments["output_directory"] = "/home/aj/PokeRap/Pokemon/"
        arguments["image_directory"] = pokemon
        response.download(arguments)
        print("Downloaded images for pokemon: " + pokemon)
    else:
        arguments["keywords"] = "\"" + pokemon + "\"" + " -shiny"
        arguments["limit"] = 100
        arguments["output_directory"] = "/home/aj/PokeRap/Pokemon/"
        arguments["image_directory"] = pokemon
        response.download(arguments)
        print("Downloaded images for pokemon: " + pokemon)

