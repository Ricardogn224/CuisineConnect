from flask import Flask, request, render_template, redirect, jsonify, url_for, session
import openai
import json
from dotenv import load_dotenv
import programmes.db_interaction as db_inter
import os
from functools import wraps
from flask import session, redirect, url_for
from flask_session import Session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('connexion'))
        return f(*args, **kwargs)
    return decorated_function

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
        type_recette = request.form["nom_recette"]
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
            engine="gpt-3.5-turbo-instruct",
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

@app.route('/recette/accompagnements', methods=['POST', 'GET'])
def get_accompagnements():
    if request.method == 'POST':
        nom_recette = request.form['nom_recette']
        # Utilisez l'API GPT-3 pour générer une réponse en fonction de la requête
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"propose 5 accompagnements pour cette recette : {nom_recette}. Accompagnements sont soît des apéritifs, des boissons ou des desserts. Chaque accompagnement doit être au format JSON avec les clés : nom_accompagnement. Les clés doivent être en minuscules. Fournir une liste contenant 5 dictionnaires représentant les accompagnements, sans texte supplémentaire avant ou après la liste.",
            max_tokens=2000
        )
        result = response.choices[0].text.strip()
        
        return jsonify(result=result)
    else:
        return render_template('index.html')
    
@app.route('/recette/liste-course', methods=['POST', 'GET'])
def get_liste_course():
    if request.method == 'POST':
        nom_recette = request.form['nom_recette']
        # Utilisez l'API GPT-3 pour générer une réponse en fonction de la requête
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"propose une liste de course des ingrédients afin de réaliser cette recette : {nom_recette}. Chaque accompagnement doit être au format JSON avec les clés : nom_ingredient. Les clés doivent être en minuscules. Fournir une liste contenant 5 dictionnaires représentant les ingredients, sans texte supplémentaire avant ou après la liste.",
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
