""" from langchain_community.utilities import SQLDatabase
from langchain.output_parsers.json import SimpleJsonOutputParser
import dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI


dotenv.load_dotenv()
def get_recipe_form(nom_recette, nombre_personnes, ingredients_disponibles) :
    json_prompt = PromptTemplate.from_template(
        "Return a JSON object with an `answer` key that answers the following question: {question}"
    )

    db = SQLDatabase.from_uri("sqlite:///database.db")

    chain = create_sql_query_chain(ChatOpenAI(temperature=0), db)
    if nom_recette == "":
        response = chain.invoke({"question": f"Donne moi l'id des recettes ou le nombre_personnes est superieur ou égale à : {nombre_personnes} , ma table s'appelle recettes.si tu ne trouve pas la recette donne une recette similaire"})
    elif nombre_personnes == "":
        response = chain.invoke({"question": f"Donne moi l'id des recettes ou le nom de {nom_recette} est dans le titre de la recette ou dans la description de la recette, ma table s'appelle recettes si tu ne trouve pas la recette donne une recette similaire."})
    elif ingredients_disponibles == "":
        response = chain.invoke({"question": f"Donne moi l'id des recette ou le nom de {nom_recette} est dans le titre de la recette ou dans la description de la recette ou celle ou le nombre_personnes est superieur ou égale à : {nombre_personnes} , ma table s'appelle recettes.si tu ne trouve pas la recette donne une recette similaire"})

    #print(db.run(response))
    return (db.run(response))

print(get_recipe_form("thieb Dinar", "", ""))


"""  """ """