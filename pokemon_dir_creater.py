import os

# location of csv and where to store images
pokemon_csv = 'D:/PokeRapper/Pokemon/data/pokemon.csv'
path = 'D:/PokeRapper/Pokemon/'


# open pokemon_csv as read only and set its variable as pokemon_data
pokemon_data = open(pokemon_csv, 'r+')
# reads the x amount of lines and stores it as str
for line in pokemon_data:
    items = line.strip().split(',')
    dir_name = items[1]
    # discard the header
    if "Name" in dir_name:
        continue
    subdir_name = None
    # Create sub directories for attempt AI to identify alternate forms etc
    if "Mega " in dir_name:
        subdir_name = "Mega " + dir_name.split("Mega")[1].strip()
        dir_name = dir_name.split("Mega")[0].strip()
    elif "Primal" in dir_name:
        subdir_name = "Primal " + dir_name.split("Primal")[1].strip()
        dir_name = dir_name.split("Primal")[0].strip()
    elif "Forme" in dir_name:
        if "Deoxys" in dir_name:
            subdir_name = "Deoxys " + dir_name.split("Deoxys")[1].strip()
            dir_name = "Deoxys"
        elif "Giratina" in dir_name:
            subdir_name = "Giratina " + dir_name.split("Giratina")[1].strip()
            dir_name = "Giratina"
        elif "Shaymin" in dir_name:
            subdir_name = "Shaymin " + dir_name.split("Shaymin")[1].strip()
            dir_name = "Shaymin"
        elif "Tornadus" in dir_name:
            subdir_name = "Tornadus " + dir_name.split("Tornadus")[1].strip()
            dir_name = "Tornadus"
        elif "Thundurus" in dir_name:
            subdir_name = "Thundurus " + dir_name.split("Thundurus")[1].strip()
            dir_name = "Thundurus"        
        elif "Landorus" in dir_name:
            subdir_name = "Landorus " + dir_name.split("Landorus")[1].strip()
            dir_name = "Landorus"
        elif "Keldeo" in dir_name:
            subdir_name = "Keldeo " + dir_name.split("Keldeo")[1].strip()
            dir_name = "Keldeo"
        elif "Meloetta" in dir_name:
            subdir_name = "Meloetta " + dir_name.split("Meloetta")[1].strip()
            dir_name = "Meloetta"
        elif "Aegislash" in dir_name:
            subdir_name = "Aegislash " + dir_name.split("Aegislash")[1].strip()
            dir_name = "Aegislash"        
        elif "Zygarde" in dir_name:
            subdir_name = "Zygarde " + dir_name.split("Zygarde")[1].strip()
            dir_name = "Zygarde"
    elif "Cloak" in dir_name:
        subdir_name = "Wormadam " + dir_name.split("Wormadam")[1].strip()
        dir_name = "Wormadam"
    elif " Rotom" in dir_name:
        subdir_name = dir_name.split("Rotom")[1].strip() + " Rotom"
        dir_name = "Rotom"
    elif "Mode" in dir_name:
        subdir_name = "Darmanitan " + dir_name.split("Darmanitan")[1].strip()
        dir_name = "Darmanitan"
    elif " Kyurem" in dir_name:
        subdir_name = dir_name.split("Kyurem")[1].strip() + " Kyurem"
        dir_name = "Kyurem"
    elif "Size" in dir_name:
        if "Pumpkaboo" in dir_name:
            subdir_name = "Pumpkaboo " + dir_name.split("Pumpkaboo")[1].strip()
            dir_name = "Pumpkaboo"
        if "Gourgeist" in dir_name:
            subdir_name = "Gourgeist " + dir_name.split("Gourgeist")[1].strip()
            dir_name = "Gourgeist"
    elif "Hoopa" in dir_name:
        subdir_name = "Hoopa " + dir_name.split("Hoopa")[2].strip()
        dir_name = "Hoopa"
    elif "Meowstic" in dir_name:
        subdir_name = "Meowstic " + dir_name.split("Meowstic")[1].strip()
        dir_name = "Meowstic"
    
    # Currently the way this is set up is that it tries making the parent directory multiple times for Pokemon with multiple
    # forms etc. Therefore, even if parent pokemon directory exists, make the alternate form subdirectory.
    try:
        os.makedirs(os.path.join(path, dir_name))
        if subdir_name is not None:
            os.makedirs(os.path.join(os.path.join(path, dir_name), subdir_name))
    except FileExistsError:
        if subdir_name is not None:
            os.makedirs(os.path.join(os.path.join(path, dir_name), subdir_name))