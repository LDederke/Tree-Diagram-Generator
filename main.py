# -- coding: UTF-8 -*-

import geopandas as gpd
from shapely.geometry import LineString, Polygon
import os
import csv
from datetime import datetime
import pandas as pd
from functools import reduce
from itertools import product


def lese_parameter_aus_datei(parameter_dateiname, zu_lesende_bezeichnungen):
    parameter = {}
    skript_verzeichnis = os.path.dirname(os.path.abspath(__file__))
    dateipfad = os.path.join(skript_verzeichnis, parameter_dateiname)

    with open(dateipfad, 'r') as datei:
        for zeile in datei:
            bezeichnung, wert = map(str.strip, zeile.split(':', 1))
            if bezeichnung in zu_lesende_bezeichnungen:
                parameter[bezeichnung] = wert
    return parameter

if __name__ == "__main__":
    parameter_dateiname = 'input_parameter.txt'

    # Parameters to be loaded
    zu_lesende_bezeichnungen = ['Project name', 'Projectpath', 'Path of the Excel file', 'Box size (height, width)', 'Box size upper Level in %', 'Box spacing', 'Level spacing']

    # Read the parameters from .txt file
    parameter = lese_parameter_aus_datei(parameter_dateiname, zu_lesende_bezeichnungen)

    # Pass project parameters to variables
    project_name = parameter.get('Project name', 'Example project')
    projectpath = parameter.get('Projectpath', 'XXXXXX')
    excel_dateipfad = parameter.get('Path of the Excel file', 'Standardpfad')
    box_size_input = parameter.get('Box size (height, width)', '3, 6')
    Box_size_upper_Level_input = parameter.get('Box size upper Level in %', '130')
    box_space_input = parameter.get('Box spacing', '2')
    Level_space_input = parameter.get('Level spacing', '4')

# Check whether it is a character string
if isinstance(box_size_input, str):
    # if not: convert the string into a list of integers
    Box_size = list(map(int, box_size_input.split(',')))
else:
    Box_size = box_size_input

# Try to convert the strings into an integer
try:
    Box_space = int(box_space_input)
except ValueError:
    print("Error: The input Box_space could not be interpreted as an integer.")

try:
    Level_space = int(Level_space_input)
except ValueError:
    print("Error: The input Level_space could not be interpreted as an integer.")

try:
    Box_size_upper_Level = int(Box_size_upper_Level_input)
except ValueError:
    print("Error: The input Box_size_upper_Level could not be interpreted as an integer.")
    
# Call up the current date and time
now = datetime.now()

# Set format for date and time (e.g. YYYYMMDD_HHMMSS)
date_time_format = now.strftime("%Y%m%d_%H%M%S")

# Create project folder
folder_name = f"{date_time_format}_{project_name}"
folder_path = os.path.join(projectpath, folder_name) 
os.makedirs(folder_path, exist_ok=True)               

# Read excel sheet 
daten = pd.read_excel(excel_dateipfad)

ueberschriften_liste = daten.columns.tolist()

# Show available headings
print("Available columns:")
for i, ueberschrift in enumerate(ueberschriften_liste):
    print(f"{i}: {ueberschrift}")

# Let the user enter the indices of the desired columns
benutzer_eingabe = input("Enter the indices of the desired columns in the desired sequence (separated by commas only): ")
ausgewaehlte_spalten_indizes = [int(index) for index in benutzer_eingabe.split(',')]
userinput_ID = input("Enter the indice of the desired ID column: ")
userinput_ID = int(userinput_ID) # Read userinput_ID as an intiger
#print("Indices of selected columns (ausgewaehlte_spalten_indizes): ", ausgewaehlte_spalten_indizes)
#print("ID-Column indice (userinput_ID): ", userinput_ID)

# Build a list with column indizes and column-ID to select dateframe
data_to_be_selected = []
for i in ausgewaehlte_spalten_indizes:
    data_to_be_selected.append(i)
data_to_be_selected.append(userinput_ID)
#print(data_to_be_selected)
# Create a data frame with the selected data
ausgewaehlte_daten = daten.iloc[:, data_to_be_selected]

# Show the selected data
#print("Selected data: ", ausgewaehlte_daten)

# Create a list with complete column names
ausgewaehlte_spalten = [ueberschriften_liste[index] for index in ausgewaehlte_spalten_indizes]
#print("Column names (ausgewaehlte_spalten): ", ausgewaehlte_spalten)

ausgewaehlte_spalten = [ueberschriften_liste[index] for index in ausgewaehlte_spalten_indizes]

# Create a lists for "Column names and attributes" and "Number of attributes per colunm"
level_attribute = []
number_attribute = []

# Iterate over the selected columns
for index, value in enumerate(ausgewaehlte_spalten):
    # Extract the unique values in the current column
    einzigartige_werte = ausgewaehlte_daten[value].unique().tolist()
    
    # Add the sublist to the list of attributes
    level_attribute.append({value: einzigartige_werte})
    number_attribute.append(len(einzigartige_werte))

    if index == len(ausgewaehlte_spalten)-1: #skip the ID column
        break

#print("Column names and attributs (level_attribute): ", level_attribute)
#print("Number of attributs per column (number_attribute): ", number_attribute)


# Get number of branches by multiplying the attributes
number_of_branches = reduce(lambda x, y: x * y, number_attribute)
#print("Total number ob branches (number_of_branches): ", number_of_branches)


Number_of_levels = len(ausgewaehlte_spalten)

#Number of branches per level buttom up
#eg number_attribute = [2, 3, 5] --> number_branch_per_level = [30, 6, 2]
number_branch_per_level = []
len_number_attributs = len(number_attribute)
for i in number_attribute:
    number = 1
    for m in range(len_number_attributs):
        number = number * number_attribute[m]
    number_branch_per_level.append(number)
    len_number_attributs -= 1
#print("Number of branches per level, buttom up :", number_branch_per_level)


# List of all combinations (banches)
attribute = [list(item.values())[0] for item in level_attribute]
all_combinations = list(product(*attribute))
#print("attribute: ", attribute)
print("all_combinations: ", all_combinations)


#List of features per box and list of IDs per branch
number_of_features = []
IDs_per_branch = []

for i in range(len(all_combinations)): #Iterate over each branch
    filtered_df = ausgewaehlte_daten
    x = []
    for index, value in enumerate(all_combinations[i]): #Iterate over each level
        #print(f"Filter: {ausgewaehlte_spalten[index]} == {value}")
        filtered_df = filtered_df[filtered_df[ausgewaehlte_spalten[index]] == value]
        anzahl_datensätze = len(filtered_df)
        x.append(anzahl_datensätze)
    number_of_features.append(x)
    id_list = filtered_df[ueberschriften_liste[userinput_ID]].tolist()
    IDs_per_branch.append(id_list)

#print("Number of features (number_of_features): ", number_of_features)
#print("ID's per branch (IDs_per_branch): ", IDs_per_branch)

# Create a list with the branches formatted
all_combinations_formatted = []

for index, value in enumerate(all_combinations):
    if len(value) > 1:
        all_combinations_formatted.append('-'.join(map(str, value)))
    else: 
        all_combinations_formatted.append(str(str, value[0]))
#print("List of branches formatted (all_combinations_formatted): ", all_combinations_formatted)


# Create a consecutive numbering of the branches
branch_ID = []
for i in range(len(all_combinations_formatted)):
    branch_ID.append(i+1)
#print("Brach ID (branch_ID): ", branch_ID)


# Write CSV with the IDs sorted by branch
def kombiniere_listen(liste): # Funktion zum Zusammenführen der inneren Listen der IDs
    return ', '.join(map(str, liste))

# Combine the lists into one list
kombinierte_liste = list(zip(branch_ID, all_combinations_formatted, map(kombiniere_listen, IDs_per_branch)))

# Path to the CSV file

csv_name = 'IDs_per_branch.csv'
csv_dateipfad = os.path.join(folder_path, csv_name)

# Define the headings
headers = ['Branch ID', 'Branch', 'IDs per Branch']

# Open the CSV file in write mode
with open(csv_dateipfad, 'w', newline='', encoding='utf-8') as csv_datei:
    # Use a tab (\t) as delimiter, this should not appear in the ID-data!
    csv_writer = csv.writer(csv_datei, delimiter='\t', quoting=csv.QUOTE_NONE)

    # Write the headings
    csv_writer.writerow(headers)

    # Write the combined data to the CSV file
    for element in kombinierte_liste:
        csv_writer.writerow(element)
#print(f'Die CSV-Datei wurde unter {csv_dateipfad} erstellt.')



#List of koordinaten and way of branch
Box_list = []
start_x = 0
start_y = 0
full_width = (Box_size[1] + Box_space)* number_of_branches # The full width of the tree

level_count = len(ausgewaehlte_spalten)
for index, value in enumerate(ausgewaehlte_spalten):
    Box_list.append([])
    path_index = 0
    for i in range(number_branch_per_level[index]):
        hight = int(Box_size[0])
        width = int(Box_size[1])
        UL = (start_x, start_y)
        UR = (start_x + width, start_y)
        OL = (start_x, start_y + hight)
        OR = (start_x + width, start_y + hight)

        pathstep = number_of_branches/number_branch_per_level[index]
        path = all_combinations[path_index][:level_count]
        Box_list[index].append([path, UL, UR, OL, OR])
        print("Pathindex: ", path_index)

        if path_index < number_of_branches:
            path_index += int(pathstep)
        else:
            pass
        start_x = start_x + Box_size[1] + Box_space

    start_y = start_y + Level_space + Box_size[0]
    Box_size = [value * Box_size_upper_Level / 100 for value in Box_size]
    if index < len(ausgewaehlte_spalten)-1:
        Box_space = (full_width - Box_size[1]* number_branch_per_level[index+1])/number_branch_per_level[index+1]
    else:
        pass
    start_x = Box_space/2
    level_count -=1

print("Box_list: ", Box_list)


# Write shapefile
for index, value in enumerate(Box_list): # Write one shapefile per level
    # Creat a list (1 to x) of branches
    ID = [] 
    for i in range(len(Box_list[index])): 
        ID.append(i+1)
    # Format the path
    Branch = [] 
    for i in range(len(Box_list[index])):
        if len(Box_list[index][i][0]) > 1:
            Branch.append('-'.join(map(str, Box_list[index][i][0])))
        else:
            Branch.append(str(Box_list[index][i][0]))
    # Create the name
    Box_Name = []
    for i in range(len(Box_list[index])):
        Box_Name.append(Box_list[index][i][0][-1])
    # Determine the number of features in this branch
    number_of_features_this_level = []
    stepsize = number_of_branches/number_branch_per_level[index]
    for i in range(len(Box_list[index])):
        m = int(i*stepsize)
        n = index+1
        number_of_features_this_level.append(number_of_features[m][-n])
    # Create the coordinates for the geometry
    geometry = []
    for i in range(len(Box_list[index])):
        geometry.append(f"POLYGON(({str(Box_list[index][i][1]).replace(',', '').replace('(', '').replace(')', '')}, {str(Box_list[index][i][2]).replace(',', '').replace('(', '').replace(')', '')}, {str(Box_list[index][i][4]).replace(',', '').replace('(', '').replace(')', '')}, {str(Box_list[index][i][3]).replace(',', '').replace('(', '').replace(')', '')}, {str(Box_list[index][i][1]).replace(',', '').replace('(', '').replace(')', '')}))")

    data = {'ID': ID,
        'Name': Box_Name,
        'Branch': Branch,
        'Num_feat': number_of_features_this_level,
        'geometry': geometry}
    
    #print("ID: ", ID)
    #print("Branches: ", Branch)
    #print("Koordinaten: ", geometry)

    # Create a GeoDataFrame with polygons
    gdf = gpd.GeoDataFrame(data, geometry=gpd.GeoSeries.from_wkt(data['geometry']))

    # Save the GeoDataFrame as a shape file
    formatted_index = "{:03d}".format(len(Box_list)-index)
    output_shapefile_name = f"{formatted_index}_{ausgewaehlte_spalten[-(index+1)]}.shp" 
    output_shapefile = os.path.join(folder_path, output_shapefile_name)
    gdf.to_file(output_shapefile, driver='ESRI Shapefile')

