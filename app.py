from flask import Flask, request, render_template, redirect, jsonify, url_for, session
import openai
import json
from dotenv import load_dotenv
import programmes.db_interaction as db_inter
import os
from functools import wraps
from flask import session, redirect, url_for
from flask_session import Session
import programmes.ask_db as ask_db
from googlesearch import search

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('connexion'))
        return f(*args, **kwargs)
    return decorated_function

def extract_numbers(input_list):
    # Check if the input list is not empty
    if input_list:
        numbers = []
        # Iterate through each tuple in the list
        for tpl in input_list:
            # Check if the tuple contains exactly one element
            if isinstance(tpl, tuple) and len(tpl) == 1:
                # Append the number inside the tuple to the result list
                numbers.append(tpl[0])
            else:
                # Handle the case where a tuple doesn't meet the criteria
                print(f"Skipping invalid tuple: {tpl}")

        return numbers
    else:
        # Return an error message or handle the case accordingly
        return "Invalid input"

def get_recipe_image_link(query):
    try:
        search_result = search(query + " recipe", num_results=1)
        return next(search_result)
    except StopIteration:
        return None

def update_json_with_image_links(recipes):
    for recipe in recipes:
        query = f"{recipe['titre']} dish"
        image_link = get_recipe_image_link(query)
        if image_link:
            recipe['image_link'] = image_link
        else:
            recipe['image_link'] = "No image available"

    return recipes

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Créer un objet OpenAI
secret_key = os.getenv("SECRET_KEY")

# Créer un objet OpenAI
openai.api_key = secret_key


def get_recipes(number):
    # Afficher la liste des recettes africaines
    recettes = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt="Propose moi {number} recettes de cuisine africaine en utilisant des ingrédients de votre choix. Chaque recette doit être au format JSON avec les clés : titre, type, description, nombre de personnes, et ingrédients. Les clés doivent être en minuscules. Veuillez fournir une liste contenant {number} dictionnaires représentant les recettes, sans texte supplémentaire avant ou après la liste.",
        max_tokens=2000
    )

    recettes = recettes.choices[0].text.strip()
    print("recettes :", recettes)
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
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Propose 5 recettes de {type_recette} pour {nombre_personnes} personnes avec les ingrédients suivants : {ingredients_disponibles}, Chaque recette doit être au format JSON avec les clés : titre, type, description, pays, nombre de personnes, et ingrédients. Les clés doivent être en minuscules. Veuillez fournir une liste contenant 5 dictionnaires représentant les recettes, sans texte supplémentaire avant ou après la liste.",
        max_tokens=2000
    )
    recettes = recettes.choices[0].text.strip()

    try:
        recettes = json.loads(recettes)
    except:
        recettes = []

    return recettes


# @app.route("/")
# def index():
#     # Afficher la liste des recettes africaines
#     recettes = get_recipes(5)
#     # Si la liste est vide, on réessaye
#     while recettes == []:
#         recettes = get_recipes(5)
#
#     print("recipes on page recettes :", recettes)
#     return render_template("recettes.html", recettes=recettes)

@app.route("/")
@login_required  
def index():
    # # Afficher la liste des recettes africaines
    # recettes = get_recipes(5)
    # # Si la liste est vide, on réessaye
    # while recettes == []:
    #     recettes = get_recipes(5)
    #
    # print("recipes on page recettes :", recettes)
    return render_template("home.html", recettes=recettes)

@app.route("/recettes", methods=["GET", "POST"])
@login_required
def recettes():
    # Récupérer les paramètres de la requête
    if request.method == "POST":
        nom_recette = str(request.form["nom_recette"])
        nombre_personnes = str(request.form["nombre_personnes"])
        ingredients_disponibles = str(request.form["ingredients_disponibles"])

        # je recupère toute les recettes dans ma base de donnée
        names = db_inter.get_all_recipes_name()
        
        
        
        if nom_recette == "" and nombre_personnes == "" and ingredients_disponibles == "":
            recettes = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=f"Voici les noms de recettes africaine :  {names} génère moi les informtions nécéssaires  consernant ces recettes de tel sorte que chaque recette doit être au format JSON avec les clés : titre, type,description, nombres de personnes, ingredients, image_link. Les clés doivent être en minuscules. La réponse attendue doit être une liste contenant 10 dictionnaires représentant les recettes, sans texte avant ou après la liste. ",
                max_tokens=2000
            )

            recettes = recettes.choices[0].text.strip()
            # list to json
            recettes = json.loads(str(recettes))
            return render_template("recettes.html", recettes=recettes)
        
        elif nom_recette == "" and nombre_personnes == "":
            recettes = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=f"Voici les noms de recettes africaine :  {names} génère moi les informtions nécéssaires  consernant les recettes pour celle qui ont dans leurs ingrédients   {ingredients_disponibles} de tel sorte que chaque la recette soit au format JSON avec les clés : titre, type,description, nombres de personnes, ingredients, image_link. Les clés doivent être en minuscules. La réponse attendue doit être une liste contenant 10 dictionnaires représentant les recettes, sans texte avant ou après la liste. ",
                max_tokens=2000
            )

            recettes = recettes.choices[0].text.strip()
            # list to json
            recettes = json.loads(str(recettes))
            return render_template("recettes.html", recettes=recettes)
        
        elif nom_recette == "" and ingredients_disponibles == "":
            recettes = []
            
            while recettes == []:
                recettes = openai.Completion.create(
                    engine="gpt-3.5-turbo-instruct",
                    prompt=f"Voici les noms de recettes africaine :  {names} génère moi les informtions nécéssaires  consernant les recettes pour celle qui sont pour {nombre_personnes} personnes de tel sorte que chaque la recette soit au format JSON avec les clés : titre, type,description, nombres de personnes, ingredients, image_link. Les clés doivent être en minuscules. La réponse attendue doit être une liste contenant 10 dictionnaires représentant les recettes, sans texte avant ou après la liste.",
                    max_tokens=2000
                )

                recettes = recettes.choices[0].text.strip()
                # list to json
                try:
                    recettes = json.loads(str(recettes))
                except:
                    recettes = []
            
            return render_template("recettes.html", recettes=recettes)
        elif nombre_personnes == "" and ingredients_disponibles == "":
            recettes = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=f"Voici les noms de recettes africaine :  {names} génère moi les informtions nécéssaires  consernant les recettes pour celle qui ont dans leurs titre ou description {nom_recette} de tel sorte que chaque la recette soit au format JSON avec les clés : titre, type,description, nombres de personnes, ingredients, image_link. Les clés doivent être en minuscules. La réponse attendue doit être une liste contenant 10 dictionnaires représentant les recettes, sans texte avant ou après la liste. ",
                max_tokens=2000
            )

            recettes = recettes.choices[0].text.strip()
            # list to json
            recettes = json.loads(str(recettes))
            return render_template("recettes.html", recettes=recettes)
        
        elif nom_recette == "":
            recettes = []
            while recettes == []:
                recettes = openai.Completion.create(
                    engine="gpt-3.5-turbo-instruct",
                    prompt=f"Voici les noms de recettes africaine :  {names} génère moi les informtions nécéssaires  consernant les recettes pour celle qui sont pour {nombre_personnes} personnes et qui ont dans leurs ingrédients {ingredients_disponibles} de tel sorte que chaque la recette soit au format JSON avec les clés : titre, type,description, nombres de personnes, ingredients, image_link. Les clés doivent être en minuscules. La réponse attendue doit être une liste contenant 10 dictionnaires représentant les recettes, sans texte avant ou après la liste.",
                    max_tokens=2000
                )

                recettes = recettes.choices[0].text.strip()
                # list to json
                try:
                    recettes = json.loads(str(recettes))
                except:
                    recettes = []
                    

            return render_template("recettes.html", recettes=recettes)
        
        elif nombre_personnes == "":
            recettes = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=f"Voici les noms de recettes africaine :  {names} génère moi les informtions nécéssaires  consernant les recettes pour celle qui ont dans leurs ingrédients {ingredients_disponibles} et qui ont dans leurs titre ou description {nom_recette} de tel sorte que chaque la recette soit au format JSON avec les clés : titre, type,description, nombres de personnes, ingredients, image_link. Les clés doivent être en minuscules. La réponse attendue doit être une liste contenant 10 dictionnaires représentant les recettes, sans texte avant ou après la liste. ",
                max_tokens=2000
            )
            
            recettes = recettes.choices[0].text.strip()
            # list to json
            recettes = json.loads(str(recettes))
            return render_template("recettes.html", recettes=recettes)
        
        elif ingredients_disponibles == "":
            recettes = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=f"Voici les noms de recettes africaine :  {names} génère moi les informtions nécéssaires  consernant les recettes pour celle qui sont pour {nombre_personnes} personnes et qui ont dans leurs titre ou description {nom_recette} de tel sorte que chaque la recette soit au format JSON avec les clés : titre, type,description, nombres de personnes, ingredients, image_link. Les clés doivent être en minuscules. La réponse attendue doit être une liste contenant 10 dictionnaires représentant les recettes, sans texte avant ou après la liste. ",
                max_tokens=2000
            )
            
            recettes = recettes.choices[0].text.strip()
            # list to json
            recettes = json.loads(str(recettes))
            return render_template("recettes.html", recettes=recettes)
        if nom_recette  != "" and nombre_personnes != "" and ingredients_disponibles != "":
            recettes = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=f"Voici les noms de recettes africaine :  {names} génère moi les informtions nécéssaires  consernant les recettes pour celle qui sont pour {nombre_personnes} personnes et qui ont dans leurs ingrédients {ingredients_disponibles} et qui ont dans leurs titre ou description {nom_recette} de tel sorte que chaque la recette soit au format JSON avec les clés : titre, type,description, nombres de personnes, ingredients, image_link. Les clés doivent être en minuscules. La réponse attendue doit être une liste contenant 10 dictionnaires représentant les recettes, sans texte avant ou après la liste.",
                max_tokens=2000
            )

            recettes = recettes.choices[0].text.strip()
            # list to json
            recettes = json.loads(str(recettes))
            return render_template("recettes.html", recettes=recettes)
    else:
        
        recettes = []
        # Afficher la liste des recettes africaines
        names = db_inter.get_all_recipes_name()
        print("names list :", names)
        
        while recettes == []:
            recettes = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=f"Voici les noms de recettes africaine :  {names} génère moi les informtions nécéssaires  consernant ces recettes de tel sorte que chaque recette doit être au format JSON avec les clés : titre, type,description, nombres de personnes, ingredients, image_link. Les clés doivent être en minuscules. La réponse attendue doit être une liste contenant 10 dictionnaires représentant les recettes, sans texte avant ou après la liste. ",
                max_tokens=2000
            )

            recettes = recettes.choices[0].text.strip()
            # list to json
            
            print("avant ",recettes)

            try:
                recettes = json.loads(str(recettes))
            except:
                recettes = []

        #recettes = update_json_with_image_links(recettes)

        print("list:", recettes)
        return render_template("recettes.html", recettes=recettes)


@app.route("/recettes/<nom_recete>", methods=["GET"])
@login_required
def recette_detail(nom_recete):
    # Obtenir la recette
    # Afficher la liste des recettes africaines
    recette = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Expliques comment faire la recette : {nom_recete} réponds en francais stp ! La recette au format JSON avec les clés : titre, nombres_personnes, ingredients, temps_cuisson, etapes. Les clés en minuscules, avec temps_cuisson contenant juste le temps total de cuisson. La réponse est une liste contenu dans un dictionnaire représentant la recette, sans texte avant ou après la liste.",
        max_tokens=4000
    )

    recette = recette.choices[0].text.strip()
        # list to json

    try:
        recette = json.loads(recette)
    except:
        recette = []

    # Afficher la page de détail de la recette
    return render_template("recette_detail.html", nom_recete=nom_recete, recette=recette)

@app.route("/recettes/<nom_recete>/recommandations", methods=["GET", "POST"]) 
@login_required
def recommandations(nom_recete):
    # # Afficher la liste des recettes africaines
    # recettes = get_recipes(5)
    # # Si la liste est vide, on réessaye
    # while recettes == []:
    #     recettes = get_recipes(5)
    #
    # print("recipes on page recettes :", recettes)
    # Afficher la liste des recettes africaines
    recettes = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Proposes 5 recettes qui proviennent de la même région que le {nom_recete} ou qui contiennent plus ou moins les mêmes ingrédients que le {nom_recete}. Chaque recette doit être au format JSON avec les clés : titre, type, description, nombre de personnes, et ingrédients. Les clés doivent être en minuscules. Veuillez fournir une liste contenant 5 dictionnaires représentant les recettes, sans texte supplémentaire avant ou après la liste. ",
        max_tokens=2000
    )

    recettes = recettes.choices[0].text.strip()
    # list to json

    print(str(recettes))

    try:
        recettes = json.loads(recettes)
    except:
        recettes = []

    print("list:", recettes)

    return render_template("recommandations.html", recettes=recettes)


@app.route('/ask', methods=['POST', 'GET'])
@login_required
def ask_chat():
    if request.method == 'POST':
        question = request.form['question']
        # Utilisez l'API GPT-3 pour générer une réponse en fonction de la requête
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"tu es cuisinier qui a 8 ans d’expérience dans la cuisine. Tu es capable de répondre à des questions sur la cuisine. tu vas repondre en français. si la question conserne la cuisine repond sinon explique que tu es cuisinier et que ce n'est pas dans tes compétences : \n\nQ: {question} ?\nA:",
            max_tokens=2000
        )
        result = response.choices[0].text.strip()
        return jsonify(result=result)
    else:
        return render_template('index.html')
    
@app.route('/chat', methods=['POST', 'GET'])
@login_required
def chat():
    if request.method == 'POST':
        question = request.form['question']
        # Utilisez l'API GPT-3 pour générer une réponse en fonction de la requête
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"Tu es un chef étoilé au guide michelin ayant une quinzaines d’années d’expérience dans le métier avec plusieurs concours culinaires gagnés à l’internationnal. Tu dois répondre en français. \n\nQ: {question}\nA:",
            max_tokens=2000
        )
        result = response.choices[0].text.strip()
        return jsonify(result=result)
    else:
        return render_template('index.html')

    
@app.route('/inscription', methods=['POST', 'GET'])	
def inscription():
    if request.method == 'POST':
        pseudo = request.form['pseudonyme']
        email = request.form['email']
        password = request.form['password']
        adresse = request.form['adresse']
        telephone = request.form['telephone']
        
        print( "Valeur rentrée :" ,pseudo, email, password, adresse, telephone)
        
        try :
            db_inter.insert_user(pseudo, email, password, adresse, telephone)
        except :
            print("erreur")

        print('insertion ok')
        return render_template('recettes.html')
    else:
        return render_template('inscription.html')
    


@app.route('/connexion', methods=['POST', 'GET'])
def connexion():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Vérification des informations de connexion
        user = db_inter.get_user(email, password)
        if user:
            # Authentification réussie, définir la session
            session['logged_in'] = True
            
            return redirect(url_for('index'))
        else:
            # Gestion des erreurs pour une connexion invalide
            print("Erreur de connexion")
            return render_template('connexion.html')
    else:
        return render_template('connexion.html')

@app.route('/deconnexion')
def deconnexion():
    # Supprimer les informations de session
    session.pop('logged_in', None)
    session.pop('user_id', None)
    # Rediriger vers la page de connexion ou toute autre page
    return redirect(url_for('connexion'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
