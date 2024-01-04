from flask import Flask, request, render_template, redirect, jsonify
import openai
import json
from dotenv import load_dotenv
import os

app = Flask(__name__)


# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Créer un objet OpenAI
secret_key = os.getenv("SECRET_KEY")

# Créer un objet OpenAI
openai.api_key = secret_key


def get_recipes(number):
    # Afficher la liste des recettes africaines
    recettes = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Propose moi {number} recettes de cuisine africaine en utilisant des ingrédients de votre choix. Chaque recette doit être au format JSON avec les clés : titre, type, nombre de personnes, et ingrédients. Les clés doivent être en minuscules. Veuillez fournir une liste contenant {number} dictionnaires représentant les recettes, sans texte supplémentaire avant ou après la liste.",
        max_tokens=2000
    )

    recettes = recettes.choices[0].text.strip()
    # list to json

    try:
        recettes = json.loads(recettes)
    except:
        recettes = []

    print("call of get recipes :", recettes)
    return recettes


def get_recipe_form(type_recette, nombre_personnes, ingredients_disponibles):
    # Générer la recette
    recettes = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Propose 5 recettes de {type_recette} pour {nombre_personnes} personnes avec les ingrédients suivants : {ingredients_disponibles}, Chaque recette doit être au format JSON avec les clés : titre, type, nombre de personnes, et ingrédients. Les clés doivent être en minuscules. Veuillez fournir une liste contenant 5 dictionnaires représentant les recettes, sans texte supplémentaire avant ou après la liste.",
        max_tokens=2000
    )
    recettes = recettes.choices[0].text.strip()

    try:
        recettes = json.loads(recettes)
    except:
        recettes = []

    return recettes


@app.route("/")
def index():
    # Afficher la liste des recettes africaines
    recettes = get_recipes(5)
    # Si la liste est vide, on réessaye
    while recettes == []:
        recettes = get_recipes(5)

    print("recipes on page recettes :", recettes)
    return render_template("recettes.html", recettes=recettes)


@app.route("/recettes", methods=["GET", "POST"])
def recettes():
    # Récupérer les paramètres de la requête
    if request.method == "POST":
        type_recette = request.form["type_recette"]
        nombre_personnes = request.form["nombre_personnes"]
        ingredients_disponibles = request.form["ingredients_disponibles"]

        recettes = get_recipe_form(type_recette, nombre_personnes,
                                   ingredients_disponibles)
        while recettes == []:
            recettes = get_recipe_form(type_recette, nombre_personnes,
                                       ingredients_disponibles)
        print("list on page /recette :", recettes)

        # Retourner la liste des recettes
        return render_template("recettes.html", recettes=recettes)
    else:
        # Afficher la liste des recettes africaines
        recettes = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Propose 5 recettes de cuisine africaines avec les ingrédients de ton choix. Chaque recette doit être au format JSON avec les clés : titre, type, nombres de personnes, ingredients. Les clés doivent être en minuscules. La réponse attendue doit être une liste contenant 10 dictionnaires représentant les recettes, sans texte avant ou après la liste. ",
            max_tokens=2000
        )

        recettes = recettes.choices[0].text.strip()
        # list to json

        try:
            recettes = json.loads(recettes)
        except:
            recettes = []

        print("list:", recettes)
        return render_template("recettes.html", recettes=recettes)


@app.route("/recettes/<nom_recete>", methods=["GET"])
def recette_detail(nom_recete):
    # Obtenir la recette
    # Afficher la liste des recettes africaines
    recette = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Explique moi comment faire la recette : {nom_recete} peut tu me repondre en francais s'il te plait !, rajoute moi le temps de cuisons entre les Etapes, parle moi en français s'il te plait !  ",
        max_tokens=4000
    )

    recette = recette.choices[0].text.strip()

    # Afficher la page de détail de la recette
    return render_template("recette_detail.html", nom_recete=nom_recete, recette=recette)


@app.route('/ask', methods=['POST', 'GET'])
def ask_chat():
    if request.method == 'POST':
        question = request.form['question']
        # Utilisez l'API GPT-3 pour générer une réponse en fonction de la requête
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"tu es cuisinier qui a 8 ans d’expérience dans la cuisine. Tu es capable de répondre à des questions sur la cuisine. tu vas repondre en français. si la question conserne la cuisine repond sionon explique que tu est cuisinier et que ce n'ai pas dans tes compétences : \n\nQ: {question} ?\nA:",
            max_tokens=2000
        )
        result = response.choices[0].text.strip()
        return jsonify(result=result)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
