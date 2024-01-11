from langchain_community.utilities import SQLDatabase
from langchain_openai import OpenAI
from langchain.output_parsers.json import SimpleJsonOutputParser
import dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()
def get_recipe_form(recette) :
    json_prompt = PromptTemplate.from_template(
        "Return a JSON object with an `answer` key that answers the following question: {question}"
    )

    db = SQLDatabase.from_uri("sqlite:///database.db")
    llm = OpenAI()

    chain = create_sql_query_chain(ChatOpenAI(temperature=0), db)
    response = chain.invoke({"question": "Donne moi l'id des recette ou le nom de {recette} est dans le titre de la recette ou dans la description de la recette, ma table s'appelle recettes."})

    print(db.run(response))
    return (db.run(response))

print(get_recipe_form("Mafé"))


