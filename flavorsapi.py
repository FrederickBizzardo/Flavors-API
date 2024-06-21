#!flask/bin/python
#from flask_cors import CORS
'''from flask import Flask, request, jsonify, abort, make_response, url_for, render_template, flash, redirect, send_file
from bs4 import BeautifulSoup

#import sqlite3
import psycopg2
import psycopg2.extras
import os
import requests
import time
import io



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key' '''

#CORS(app, resources={r"/*": {"orgins": "*"}})

#in_memory_datastore = {
#   "COBOL": {"name": "COBOL", "publication_year": 1960, "contribution": "record data"},
#   "ALGOL": {"name": "ALGOL", "publication_year": 1958, "contribution": "scoping and nested functions"},
#   "APL": {"name": "APL", "publication_year": 1962, "contribution": "array processing"},
#   "BASIC": {"name": "BASIC", "publication_year": 1964, "contribution": "runtime interpretation, office tooling"},
#   "PL": {"name": "PL", "publication_year": 1966, "contribution": "constants, function overloading, pointers"},
#   "SIMULA67": {"name": "SIMULA67", "publication_year": 1967,
#                "contribution": "class/object split, subclassing, protected attributes"},
#   "Pascal": {"name": "Pascal", "publication_year": 1970,
#              "contribution": "modern unary, binary, and assignment operator syntax expectations"},
#   "CLU": {"name": "CLU", "publication_year": 1975,
#           "contribution": "iterators, abstract data types, generics, checked exceptions"},
#}

#@app.route('/programming_languages', methods=['GET', 'POST'])
#def programming_languages_route():
#   if request.method == 'GET':
#       return list_programming_languages()
#   elif request.method == "POST":
#       return create_programming_language(request.get_json(force=True))

#def list_programming_languages():
#   before_year = request.args.get('before_year') or '30000'
#   after_year = request.args.get('after_year') or '0'
#   qualifying_data = list(
#       filter(
#           lambda pl: int(before_year) > pl['publication_year'] > int(after_year),
#           in_memory_datastore.values()
#       )
#   )

#   return {"programming_languages": qualifying_data}

#def create_programming_language(new_lang):
#   language_name = new_lang['name']
#   in_memory_datastore[language_name] = new_lang
#   return new_lang

#@app.route('/programming_languages/<programming_language_name>', methods=['GET', 'PUT', 'DELETE'])
#def programming_language_route(programming_language_name):
#   if request.method == 'GET':
#       return get_programming_language(programming_language_name)
#   elif request.method == "PUT":
#       return update_programming_language(programming_language_name, request.get_json(force=True))
#   elif request.method == "DELETE":
#       return delete_programming_language(programming_language_name)

#def get_programming_language(programming_language_name):
#   return in_memory_datastore[programming_language_name]

#def update_programming_language(lang_name, new_lang_attributes):
#   lang_getting_update = in_memory_datastore[lang_name]
#   lang_getting_update.update(new_lang_attributes)
#   return lang_getting_update

#def delete_programming_language(lang_name):
#   deleting_lang = in_memory_datastore[lang_name]
#   del in_memory_datastore[lang_name]
#   return deleting_lang


#def connect_to_db():
#    conn = sqlite3.connect("flavor_api_database.db")
#    conn.row_factory = sqlite3.Row
#    print("Connecting to database")
#    return conn

#def create_db_table():
#    try:
#        conn = connect_to_db()
#        conn.execute('''
#            CREATE TABLE recipes (
#                id INT PRIMARY KEY NOT NULL,
#                title VARCHAR(155) NOT NULL,
#                ingredients VARCHAR(155),
#                servings CHAR(20), 
#                instructions VARCHAR(255)
#            );
#        ''')
#        conn.commit()
#        print("Recipe table created successfully")
#    except:
#        print("Recipe table creation failed")
#    finally:
#        conn.close()

#def insert_recipe(recipe):
#    inserted_recipes = {}
#    try:
#        conn = connect_to_db()
#        cur = conn.cursor()
#        cur.execute("INSERT INTO recipes (id, title, ingredients, servings, instructions) VALUES(?, ?, ?, ?, ?)", (recipe['id'], recipe['title'], recipe['ingredients'], recipe['servings'], recipe['instructions'], recipe['instructions']))
#        conn.commit()
#        inserted_recipes = get_recipe_by_id(cur.lastrowid)
#        print ('inserted')
#    except:
#        conn.rollback()
#    finally:
#        conn.close()
#    return inserted_recipes

#def get_recipe():
#    recipes = []
#    try: 
#        conn = connect_to_db()
#        conn.row_factory = sqlite3.Row
#        cur = conn.cursor()
#        cur.execute("SELECT * FROM recipes")
#        rows = cur.fetchall()
    
#        for i in rows:
#            recipe = {}
#            recipe["id"] = i["id"]
#            recipe["title"] = i["title"]
#            recipe["ingredients"] = i["ingredients"]
#            recipe["servings"] = i["servings"]
#            recipe["instructions"] = i["nstructions"]
#            recipes.append(recipe)
#    except:
#        recipes = []

#    return recipes

#def get_recipe_by_id(title):
#    recipe = {}
#    try:
#        conn = connect_to_db()
#        conn.row_factory = sqlite3.Row
#        cur = conn.cursor()
#        cur.execute("SELECT * FROM recipes WHERE title = ?", (title,))
#        row = cur.fetchone()

#        recipe["id"] = row["id"]
#        recipe["title"] = row["title"]
#        recipe["ingredients"] = row["ingredients"]
#        recipe["servings"] = row["servings"]
#        recipe["instructions"] = row["instructions"]
#    except:
#        recipe = {}

#    return recipe

#recipes = []

#recip1 =    {
#      "title":"Stracciatella (Italian Wedding Soup)",
#      "ingredients":"3 1/2 c Chicken broth; homemade|1 lb Fresh spinach; wash/trim/chop|1 Egg|1 c Grated parmesan cheese; --or--|1 c Romano cheese; freshly grated|Salt and pepper; to taste",
#      "servings":"4 servings",
#      "id": 1,
#      "instructions":"Bring 1 cup of the broth to a boil. Add spinach and cook until softened but still bright green. Remove spinach with a slotted spoon and set aside. Add remaining broth to pot. Bring to a boil. Meanwhile, beat egg lightly with a fork. Beat in 1/4 cup of cheese. When broth boils pour in egg mixture, stirring constantly for a few seconds until it cooks into 'rags.'' Add reserved spinach, salt and pepper. Serve immediately, passing remaining cheese. NOTES: Someone asked for this recipe a while back. I believe this soup, known as 'Stracciatella' is synonymous with Italian Wedding Soup, however, I seem to remember from I-don't-know-where that Italian Wedding Soup is the same as this but with the addition of tiny meatballs." 
#    }
#recip2 =      {
#      "title": "Need to find a good Python tutorial on the web",
#      "ingredients": "Stuff",
#      "servings": "4 servings",
#      "id": 2,
#      "instructions": "Learn Python"
#    }

#recipes.append(recip1)
#recipes.append(recip2)

#@app.route('/flavors/api/recipes', methods=['GET'])
#def api_recipe_list():
#  return jsonify(get_recipe())

#@app.route('/flavors/api/recipes/<title>', methods=['GET'])
#def api_recipes_list(title):
#  return jsonify(get_recipe_by_id(title))

#@app.route('/flavors/api/recipes/add', methods=['POST'])
#def api_add_recipe_list():
#    recipe = request.get_json()
#    return jsonify(insert_recipe(recipe))
'''try: 
    #url = 'https://www.recipe-free.com/recipes/easy-swedish-meatballs---jamie-oliver-recipe/129381'
    #url = 'https://www.recipe-free.com/recipes/best-african-vegetarian-stew/129364'
    #url = 'https://www.recipe-free.com/recipes/real-coconut-chicken-tenders-recipe-joel-robuchon-recipe/129450'
    #result = requests.get(url).text

    #url = 'https://www.recipe-free.com/recipes/easy-swedish-meatballs---jamie-oliver-recipe/129381'


    #result = requests.get(url).text

    #doc = BeautifulSoup(result, 'html.parser')


    #rtitle = doc.find('h1', {'class': 'red'}).text.strip()
    #ringredients = doc.find('div', {'class': 'col-md-12 for-padding-col'}).find_all('p')[0].text.strip()
    #rservings = doc.find('div', {'class': 'times'}).findAll('div', {'class': 'times_tab'})[1].findAll('div', {'class': 'f12 f12'})[1].text.strip()
    #rinstructions = doc.find('div', {'class': 'col-md-12 for-padding-col'}).find_all('p')[1].text.strip()
    #print(f'title: {rtitle}')
    #print(f'ingredients: {ringredients}')
    #print(f'servings: {rservings}')
    #print(f'instructions: {rinstructions}')

    page = 1
    url_no = 1
    titles = []
    links = []
    links_dict = {}

    while page != 7:
        url = f"https://www.recipe-free.com/categories/meat-recipes/{page}"
        # print(url)
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, "lxml")
        for a in soup.find('div', {'class': 'category_content centerindent for-this'}).findAll('a', {'class': 'day'}):
            titles.append(a.get_text(strip=True))
            links.append(a.get('href'))
            # print(titles)
        page = page + 1
    for title in titles[:80]:
        print(title)
    for i, link in enumerate(links[:120], url_no):
        # print(f'url {url_no}: {link}')
        name = f'url {url_no}'
        links_dict = {name: link}
        # links_dict = {f'url {url_no}': link}
        url_no += 1
        # for dict in links_dict:
        # print(links_dict)
        print(links_dict[name])
        # code to get info from each link stored in links_dict
        url_grapper = links_dict[name]
        result = requests.get(url_grapper).text
        doc = BeautifulSoup(result, 'html.parser')
        # Extract image URL
        image_tag = doc.find('div', {'class': 'col-md-4 col-sm-4'}).findAll('div')[0].findAll('img')[0]
        image_url = image_tag['src']
        image_url_fixed = image_url.replace('../..', '')
        base_url = 'https://www.recipe-free.com'
        rimage_url = base_url + image_url_fixed
        try:
            rimage = requests.get(rimage_url).content  # Fetch image data
        except requests.exceptions.RequestException as e:
            print(f"Error! Failed to fetch image from {rimage_url}: {e}")
            rimage = None
        # Extract other details
        rtitle = doc.find('h1', {'class': 'red'}).text.strip()
        ringredients = doc.find('div', {'class': 'col-md-12 for-padding-col'}).find_all('p')[0].text.strip()
        rservings = doc.find('div', {'class': 'times'}).findAll('div', {'class': 'times_tab'})[1].findAll('div', {
            'class': 'f12 f12'})[1].text.strip()
        rinstructions = doc.find('div', {'class': 'col-md-12 for-padding-col'}).find_all('p')[1].text.strip()

        #print(f'title: {rtitle}')
        #print(f'ingredients: {ringredients}')
        #print(f'servings: {rservings}')
        #print(f'instructions: {rinstructions}')
        print(f'images: {rimage_url}')


        try:
            DATABASE_URL = os.environ['DATABASE_URL']
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            conn = psycopg2.connect(
                host="localhost",
                database="flavors_api",
                user=os.environ['DB_USERNAME'],
                password=os.environ['DB_PASSWORD'])

        try:
            cur = conn.cursor()'''
            #query = '''INSERT INTO recipes(title, ingredients, servings, instructions, image) VALUES(%s, %s, %s, %s, %s)'''
            #record_to_insert = (rtitle, ringredients, rservings, rinstructions, psycopg2.Binary(rimage) if rimage else None)
            #cur.execute(query, record_to_insert)
            #conn.commit()
            #conn.close()
        #except Exception as e:
            #print(f"Failed to insert data: {e}")

#except Exception as e:
    #print(f"Failed to establish a new connection: {e}")


#def in_data():




#conn = psycopg2.connect(DATABASE_URL, sslmode='require')

#Row and column in database tables


'''def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Home screen
@app.route('/', methods=['GET'])
def home():
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost", 
            database="flavors_api",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])

    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    #all_recipes = cur.execute('SELECT * FROM recipes;').fetchall()
    cur.execute('SELECT * FROM recipes;')
    recipes = cur.fetchall()

    return render_template('index.html', recipes=recipes)

def get_recipe_id(rep_id):
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost", 
            database="flavors_api",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])

    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM recipes WHERE rep_id = %s', (rep_id,))
    recipes = cur.fetchone()

    conn.close()
    if recipes is None:
        abort(404)
    return recipes


@app.route('/<int:rep_id>')
def recipe_id(rep_id):
    recipes = get_recipe_id(rep_id)
    return render_template('recipes.html', recipes=recipes)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        servings = request.form['servings']
        instructions = request.form['instructions']
    

        if not title:
            flash('Title is required!')
        if not ingredients:
            flash('Ingredients is required!')
        if not servings:
            flash('Servings is required!')
        if not instructions:
            flash('Instructions is required!')
        
        else:
            try:
                DATABASE_URL = os.environ['DATABASE_URL']
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            except:
                conn = psycopg2.connect(
                    host="localhost", 
                    database="flavors_api",
                    user=os.environ['DB_USERNAME'],
                    password=os.environ['DB_PASSWORD'])
            cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)      
            cur.execute('INSERT INTO recipes (title, ingredients, servings, instructions) VALUES (%s, %s, %s, %s)',
                         (title, ingredients, servings, instructions))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))
    
    # Fix code below, ingredients add button triggers instructions button
    ingredients = []
    #instructions = []
    
    ingredients = ingredients.append(ingredients) 
    ingredients = request.form.get('ingredients') 
    
    
    #instructions = instructions.append(instructions) 
    #instructions = request.form.get('instructions') 
    return render_template('create.html', ingredients=ingredients)
 
@app.route('/flavors/api/recipes', methods=['GET'])
def api_all():
    #conn = sqlite3.connect('flavor_api_database.db')
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost", 
            database="flavors_api",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])
        #host="localhost", 
        #database="flavors_api",
        #DB_USERNAME=os.environ['DB_USERNAME'],
        #DB_PASSWORD=os.environ['DB_PASSWORD']
        
        #URL = os.environ.get('postgres://etryrrveyngcvx:7eb31e76ed3b8452749bada81b9058ee51cc902b7ea996b3a2b566ab841dbe5b@ec2-44-198-82-71.compute-1.amazonaws.com:5432/ddskfvmrts9ipg')
        #DATABASE_URL=os.environ.get('postgres://etryrrveyngcvx:7eb31e76ed3b8452749bada81b9058ee51cc902b7ea996b3a2b566ab841dbe5b@ec2-44-198-82-71.compute-1.amazonaws.com:5432/ddskfvmrts9ipg -a flavorsapi')
        
    #conn.row_factory = dict_factory
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    #all_recipes = cur.execute('SELECT * FROM recipes;').fetchall()
    cur.execute('SELECT * FROM recipes;')
    all_recipes = cur.fetchall()
    return jsonify({'recipes': all_recipes})
    #return validate(instance={'recipes': cur}, schema=all_recipes)

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404!</h1><p>Resource not found.</p>", 404

# GET Requests
@app.route('/flavors/api/recipes', methods=['GET'])
def api_filter():
    query_params = request.args

    rep_id = query_params.get('rep_id')
    title = query_params.get('title')
    ingredients = query_params.get('ingredients')
    servings = query_params.get('servings')
    instructions = query_params.get('instructions')

    query = "SELECT * FROM recipes WHERE"
    to_filter = []

    if rep_id:
        query += 'rep_id=? AND' 
        to_filter.append(rep_id)
    if title:
        query += 'title=? AND'
        to_filter.append(title)
    if ingredients:
        query += 'ingredients=? AND'
        to_filter.append(ingredients)
    if servings:
        query += 'servings=? AND'
        to_filter.append(servings)
    if instructions:
        query += 'instructions=? AND'
        to_filter.append(instructions)
    if not (rep_id or title or ingredients or servings or instructions):
        return page_not_found(404)

    query = query[:-4] + ';'

    #conn = sqlite3.connect('flavor_api_database.db')
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost", 
            database="flavors_api",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])

    #conn.row_factory = dict_factory
    #cur = conn.cursor()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    cur.execute(query, to_filter)
    results = cur.fetchall()
    return jsonify(results)

# Inserted user recipe(s)
def insert_recipe(rep_id, title, ingredients, servings, instructions):
    #conn = sqlite3.connect('flavor_api_database.db')
    conn = get_db_connection()
    cur = conn.cursor()
    #cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    statement = "INSERT INTO recipes(rep_id, title, ingredients, servings, instructions) VALUES(%s, %s, %s, %s, %s)"
    cur.execute(statement, [rep_id, title, ingredients, servings, instructions])
    conn.commit()
    return True

# Posted user recipe(s)
@app.route('/flavors/api/recipes', methods=['GET', 'POST'])
def api_post():
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost", 
            database="flavors_api",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])

    recipes = request.get_json()
 
    #rep_id = request.json['rep_id']
    
    title = request.json['title']
    ingredients = request.json.get('ingredients', "")
    servings = request.json.get('servings', "")
    instructions = request.json.get('instructions', "")
    #conn = sqlite3.connect('flavor_api_database.db')
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    #conn.execute('INSERT INTO recipes(id, title, ingredients, servings, instructions) VALUES(?, ?, ?, ?, ?)', (id, title, ingredients, servings, instructions))
    cur.execute('INSERT INTO recipes(title, ingredients, servings, instructions) VALUES(%s, %s, %s, %s);', (title, ingredients, servings, instructions))
    conn.commit()
    conn.close()
    return jsonify({'recipe': recipes}), 201

# Filter through recipes database
#def get_recipe_by_id(rep_id):
    #conn = sqlite3.connect('flavor_api_database.db')
#    conn = psycopg2.connect(
#        host="localhost", 
#        database="flavors_api",
#        user=os.environ['DB_USERNAME'],
#        password=os.environ['DB_PASSWORD'])
#    cursor = conn.cursor()
#    statement = "SELECT rep_id, title, ingredients, servings, instructions FROM recipes WHERE rep_id = ?"
#    cursor.execute(statement, [rep_id])
#    return cursor.fetchone()

# Access specific recipe by id
@app.route('/flavors/api/recipes/<rep_name>', methods=['GET'])
def get_recipes(rep_name):
    #Old code
    #========
      #conn = psycopg2.connect(
        #host="localhost", 
        #database="flavors_api",
        #user=os.environ['DB_USERNAME'],
        #password=os.environ['DB_PASSWORD'])
    #cur = conn.cursor()
    #cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    #statement = "SELECT rep_id, title, ingredients, servings, instructions FROM recipes WHERE rep_id = ?"
    #cur.execute("SELECT rep_id, title, ingredients, servings, instructions FROM recipes WHERE rep_id = %s", [rep_id])
    #recipe = cur.fetchone()
    #recipe = get_recipe_by_id(rep_id)
    #return jsonify({'recipe': recipe}) #can change array position from 0 - 4 
    #original return jsonify({'recipe': recipe})

    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost", 
            database="flavors_api",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])

    

    #cur = conn.cursor()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    #statement = "SELECT rep_id, title, ingredients, servings, instructions FROM recipes WHERE rep_id = ?"
    #cur.execute("SELECT rep_id, title, ingredients, servings, instructions FROM recipes WHERE title = %s", [rep_name])
    cur.execute("SELECT * FROM recipes;")
    recipes = cur.fetchall()
    
    # .casefold ignores case strings (Whether uppercase or lower)
    recipe = [recipe for recipe in recipes if rep_name.casefold() in recipe['title'].casefold() or rep_name.casefold() in recipe['ingredients'].casefold()]
    #for recipe in recipes:
    #    if rep_name in recipes:
    #        break
        
    
    return jsonify({'recipe': recipe}) #can change array position from 0 - 4          
    #original return jsonify({'recipe': recipe})

# Connect to database
def get_db_connection():
    #conn = sqlite3.connect('flavor_api_database.db')
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost", 
            database="flavors_api",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])
    #conn.row_factory = sqlite3.Row
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    
    print("Connecting to database...")
    return cur

def get_recipe(rep_name):
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost", 
            database="flavors_api",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])
    post = conn.execute('SELECT *FROM recipes WHERE title = %s', {'recipe': rep_name}).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

# Modify recipe
@app.route("/flavors/api/recipes/<int:rep_id>", methods=["PUT"])
def update_recipe(rep_id):
    recipes_edit = request.get_json()
    #code to update recipe in database by id (rep_id) postgresql using psycopg2.connect
    #conn = sqlite3.connect('flavor_api_database.db')

    #rep_id = request.json['rep_id']
    #title = request.json.get('title', '')
    #ingredients = request.json.get('ingredients', "")
    #servings = request.json.get('servings', "")
    #instructions = request.json.get('instructions', "")
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        db = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        db = psycopg2.connect(
            host="localhost", 
            database="flavors_api",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])

    cursor = db.cursor()
    cursor.execute("UPDATE recipes SET title = %s, ingredients = %s, servings = %s, instructions = %s WHERE rep_id = %s", (recipes_edit['title'], recipes_edit['ingredients'], recipes_edit['servings'], recipes_edit['instructions'], rep_id))
  
    #statement =  "UPDATE recipes SET title = %s, ingredients = %s, servings = %s, instructions = %s WHERE rep_id = %s"
    #cursor.execute(statement, [title, ingredients, servings, instructions, rep_id])
    db.commit()
    return jsonify({'recipe': recipes_edit}), 201

# Delete a recipe
@app.route("/flavors/api/recipes/<int:rep_id>", methods=['DELETE'])
def delete_recipe(rep_id):
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        db = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        db = psycopg2.connect(
            host="localhost", 
            database="flavors_api",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])

    cursor = db.cursor()
    statement = "DELETE FROM recipes WHERE rep_id = %s"
    cursor.execute(statement, [rep_id])
    db.commit()
    return ('Deleted'), 201


@app.route('/recipe_image/<int:id>')
def recipe_image(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT image FROM recipes WHERE id = %s", (id,))
    image_data = cur.fetchone()
    conn.close()

    if image_data is None or image_data[0] is None:
        abort(404)

    return send_file(
        io.BytesIO(image_data[0]),
        mimetype='image/jpeg',  # or the appropriate mime type
        as_attachment=False,
        download_name='recipe_image.jpg'  # or a meaningful name
    )'''

from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, abort
from bs4 import BeautifulSoup
import psycopg2
import psycopg2.extras
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

def get_db_connection():
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost",
            database="flavors_api",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])
    return conn

def fetch_recipe_data(url):
    response = requests.get(url)
    doc = BeautifulSoup(response.text, 'html.parser')
    try:
        image_tag = doc.find('div', {'class': 'col-md-4 col-sm-4'}).find('img')
        image_url = image_tag['src'].replace('../..', '')
        base_url = 'https://www.recipe-free.com'
        rimage_url = base_url + image_url
        rimage = requests.get(rimage_url).content
    except Exception as e:
        print(f"Error fetching image: {e}")
        rimage = None
        rimage_url = None

    rtitle = doc.find('h1', {'class': 'red'}).text.strip()
    ringredients = doc.find('div', {'class': 'col-md-12 for-padding-col'}).find_all('p')[0].text.strip()
    rservings = doc.find('div', {'class': 'times'}).findAll('div', {'class': 'times_tab'})[1].findAll('div', {'class': 'f12 f12'})[1].text.strip()
    rinstructions = doc.find('div', {'class': 'col-md-12 for-padding-col'}).find_all('p')[1].text.strip()

    return {
        "title": rtitle,
        "ingredients": ringredients,
        "servings": rservings,
        "instructions": rinstructions,
        "image_url": rimage_url,
        "image": rimage
    }

def insert_recipe(recipe):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        query = '''INSERT INTO recipes(title, ingredients, servings, instructions, image) VALUES(%s, %s, %s, %s, %s)'''
        cur.execute(query, (recipe['title'], recipe['ingredients'], recipe['servings'], recipe['instructions'], psycopg2.Binary(recipe['image']) if recipe['image'] else None))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Failed to insert data: {e}")
        conn.rollback()
        cur.close()
        conn.close()

@app.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM recipes')
    recipes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', recipes=recipes)

@app.route('/<int:rep_id>')
def recipe_id(rep_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM recipes WHERE rep_id = %s', (rep_id,))
    recipe = cur.fetchone()
    cur.close()
    conn.close()
    if recipe is None:
        abort(404)
    return render_template('recipes.html', recipe=recipe)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        servings = request.form['servings']
        instructions = request.form['instructions']

        if not title:
            flash('Title is required!')
        elif not ingredients:
            flash('Ingredients are required!')
        elif not servings:
            flash('Servings are required!')
        elif not instructions:
            flash('Instructions are required!')
        else:
            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute('INSERT INTO recipes (title, ingredients, servings, instructions) VALUES (%s, %s, %s, %s)',
                        (title, ingredients, servings, instructions))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('home'))

    return render_template('create.html')

@app.route('/flavors/api/recipes', methods=['GET'])
def api_all():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM recipes')
    all_recipes = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'recipes': all_recipes})

@app.route('/flavors/api/recipes', methods=['GET'])
def api_filter():
    query_params = request.args

    rep_id = query_params.get('rep_id')
    title = query_params.get('title')
    ingredients = query_params.get('ingredients')
    servings = query_params.get('servings')
    instructions = query_params.get('instructions')
    image = query_params.get('image')

    query = "SELECT * FROM recipes WHERE"
    to_filter = []

    if rep_id:
        query += ' rep_id=%s AND'
        to_filter.append(rep_id)
    if title:
        query += ' title=%s AND'
        to_filter.append(title)
    if ingredients:
        query += ' ingredients=%s AND'
        to_filter.append(ingredients)
    if servings:
        query += ' servings=%s AND'
        to_filter.append(servings)
    if instructions:
        query += ' instructions=%s AND'
        to_filter.append(instructions)
    if image:
        query += ' image=%s AND'
        to_filter.append(image)
    if not (rep_id or title or ingredients or servings or instructions or image):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(query, to_filter)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(results)

@app.route('/flavors/api/recipes', methods=['POST'])
def api_post():
    recipes = request.get_json()

    title = recipes['title']
    ingredients = recipes.get('ingredients', "")
    servings = recipes.get('servings', "")
    instructions = recipes.get('instructions', "")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('INSERT INTO recipes (title, ingredients, servings, instructions) VALUES (%s, %s, %s, %s)',
                (title, ingredients, servings, instructions))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'recipe': recipes}), 201

@app.route('/flavors/api/recipes/<rep_name>', methods=['GET'])
def get_recipes(rep_name):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM recipes;")
    recipes = cur.fetchall()
    cur.close()
    conn.close()

    filtered_recipes = [recipe for recipe in recipes if rep_name.casefold() in recipe['title'].casefold() or rep_name.casefold() in recipe['ingredients'].casefold()]
    if not filtered_recipes:
        abort(404)
    return jsonify(filtered_recipes)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404!</h1><p>Resource not found.</p>", 404

@app.route('/image/<int:id>')
def image(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT image FROM recipes WHERE rep_id = %s', (id,))
    image_data = cur.fetchone()[0]
    cur.close()
    conn.close()
    if not image_data:
        abort(404)
    return app.response_class(image_data, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)



# Posted user recipe(s)
#@app.route('/flavors/api/recipes', methods=['GET', 'POST'])
#def api_recipe_request():    

#from flask_httpauth import HTTPBasicAuth

#auth = HTTPBasicAuth()   

#@auth.get_password
#def get_password(username):
#    if username == 'fred':
#        return 'python'
#    return None