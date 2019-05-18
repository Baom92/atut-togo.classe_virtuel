import json
import uuid

import requests
from bs4 import BeautifulSoup

from repositories.models import Etape
from repositories.models import Recette
from repositories.models import mongoConnection

collection = mongoConnection("localhost", "demo", "recette")

class ScrappingRecipe:
    def __init__(self, url, scrapping_parameters, document):

        self.url = url
        self.ingredients_tag = scrapping_parameters["ingredients_tag"]
        self.ingredients_class = scrapping_parameters["ingredients_class"]
        self.ingredients_quantity_tag = scrapping_parameters["ingredients_quantity_tag"]
        self.ingredients_quantity_class = scrapping_parameters["ingredients_quantity_class"]
        self.ingredients_name_tag = scrapping_parameters["ingredients_name_tag"]
        self.ingredients_name_class = scrapping_parameters["ingredients_name_class"]
        self.preparation_tag = scrapping_parameters["preparation_tag"]
        self.preparation_class = scrapping_parameters["preparation_class"]
        self.nom_tag = scrapping_parameters["nom_tag"]
        self.nom_class = scrapping_parameters["nom_class"]
        self.nombre_personnes_tag = scrapping_parameters["nombre_personnes_tag"]
        self.nombre_personnes_class = scrapping_parameters["nombre_personnes_class"]
        self.temps_preparation_tag = scrapping_parameters["temps_preparation_tag"]
        self.temps_preparation_class = scrapping_parameters["temps_preparation_class"]
        self.temps_cuisson_tag = scrapping_parameters["temps_cuisson_tag"]
        self.temps_cuisson_class = scrapping_parameters["temps_cuisson_class"]
        self.temps_total_tag = scrapping_parameters["temps_total_tag"]
        self.temps_total_class = scrapping_parameters["temps_total_class"]
        self.document = document

    def getPreparationEtape(self):
        preparation_document = self.document.find_all(self.preparation_tag, class_=self.preparation_class)
        preparation_list = []
        index = 1
        for elmt in preparation_document:
            contenu = elmt.text.split("Etape " + str(index))[-1].strip()
            etape = Etape(index, contenu)
            preparation_list.append(etape.__dict__)
            index = index + 1
        return preparation_list

    def getIngredientList(self):
        ingredients_document = self.document.find_all(self.ingredients_tag, class_=self.ingredients_class)
        ingredient_list = []
        for elmt in ingredients_document:
            quantite = elmt.find(self.ingredients_quantity_tag, class_=self.ingredients_quantity_class).string
            ingredient = elmt.find(self.ingredients_name_tag, class_=self.ingredients_name_class).string

            if quantite is None:
                ingredient_list.append(ingredient.strip())
            else:
                ingredient_list.append(quantite.strip() + " " + ingredient.strip())
        return ingredient_list

    def getSingleData(self):
        nom = self.document.find(self.nom_tag, class_=self.nom_class).string.strip()
        nombre_personnes = self.document.find(self.nombre_personnes_tag,
                                              class_=self.nombre_personnes_class).string.strip()
        temps_preparation = self.document.find(self.temps_preparation_tag,
                                               class_=self.temps_preparation_class).text.split("Prép.\xa0:")[-1].strip()
        temps_cuisson = self.document.find(self.temps_cuisson_tag,
                                           class_=self.temps_cuisson_class).text.split("Cuisson\xa0:")[-1].strip()
        temps_total = self.document.find(self.temps_total_tag,
                                         class_=self.temps_total_class).string.strip()

        return nom, nombre_personnes, temps_preparation, temps_cuisson, temps_total


def getData(url, scrapping_parameters):
    soup_document = BeautifulSoup(requests.get(url).text, 'html.parser')
    scrappingRecipe = ScrappingRecipe(url, scrapping_parameters, soup_document)

    preparation_list = scrappingRecipe.getPreparationEtape()
    ingredient_list = scrappingRecipe.getIngredientList()
    nom, nombre_personnes, temps_preparation, temps_cuisson, temps_total = scrappingRecipe.getSingleData()

    recette = Recette(str(uuid.uuid4()), nom, nombre_personnes, temps_preparation, temps_cuisson, temps_total,
                      ingredient_list, preparation_list)
    return recette


if __name__ == '__main__':
    main_url = "https://www.marmiton.org/recettes/selection_afrique.aspx"
    with open("../ressources/web_site_parameters.json", 'r') as fich_p:
        parameters = json.loads(fich_p.read())
        soup_document = BeautifulSoup(requests.get(main_url).text, 'html.parser')
        recipe_cards = soup_document.find_all("a", class_="recipe-card-link")
        for link in recipe_cards:
            recette = getData(link.get('href'), parameters)
            collection.insert_one(recette.__dict__)
