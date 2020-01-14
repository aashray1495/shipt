import requests


# Initiate lists
total_results = []    # Grab the search results
response = requests.get("https://swapi.co/api/people/")
data = response.json()

# Store results of first page
total_results = total_results + data['results']

# Keep visiting all pages since we are only reading one page at a time
while data['next'] is not None:
    print("pulling data from page", data['next'])
    response = requests.get(data['next'])
    data = response.json()
    # Store the current page of results
    total_results = total_results + data['results']


person_dict_ship = {}
person_dict_planet = {}
species_dict={}
for person in total_results:
    #dict for ships
    person_dict_ship[person["name"].encode('utf-8')]= [starship.encode('utf-8') for starship in person["starships"]]
    #dict for planets
    person_dict_planet[person["name"].encode('utf-8')]= [person["homeworld"].encode('utf-8')]

#function to get value from url inside the dictionary
def getval_from_url(dic):
    for key,value in dic.items():
        for v in value:
            #only if url exists i.e. starship/planet exists
            if v:
                #get all values
                a=requests.get(v).json()
                #get name of ships/planets from json collected
                dic[key]=a['name'].encode('utf-8')
    return dic

print("List of ships for every Person: /n", getval_from_url(person_dict_ship))
print("List of planets for every Person: /n", getval_from_url(person_dict_planet))


# Function for getting multiplanet_species_list
def get_multiplanetspecies():
    page=[]
    response = requests.get("https://swapi.co/api/species/")
    data = response.json()
    page=page+data['results']
    while data['next'] is not None:
        print("pulling data from species page", data['next'])
        response = requests.get(data['next'])
        data = response.json()
        # Store the current page of results
        page = page + data['results']
    for document in page:
        species_dict[document["name"].encode('utf-8')] = document["homeworld"]
    print('Dict for species and their planets', species_dict)

    multiplanet_species_list=[]
    for key,value in species_dict.items():
        if not value:
                multiplanet_species_list.append(key)

    print('Species living on multiple planet:', multiplanet_species_list)

#comment out if you do not want to get multiplanet species
get_multiplanetspecies()
