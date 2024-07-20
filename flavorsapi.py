#!flask/bin/python
# from flask_cors import CORS
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, abort, session, send_file
from bs4 import BeautifulSoup
from functools import wraps
import psycopg2
import psycopg2.extras
import requests
import os
import base64
import random
import datetime
import io


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

'''def get_db_connection():'''
'''try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost",
            database="flavors_api",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])
    return conn'''

'''def fetch_recipe_data(url):'''

app.config['DEBUG'] = os.getenv('FLASK_DEBUG', '0') == '1'
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')


categories = [
    "meat", "dessert", "fish", "vegetable", "rice", "appetizers", "pasta",
    "pizza-and-pie", "egg-and-omelette", "seafood", "salad", "bakery-and-bread",
    "sandwich", "soup", "sauce", "drink-and-cocktail", "ideas-for-dinner"
]

base_url = "https://www.recipe-free.com"
max_links_per_category = 120

try:
    session = requests.Session()  # Use a session to keep connections alive

    for category in categories:
        titles = []
        links = []

        for page in range(1, 7):
            url = f"{base_url}/categories/{category}-recipes/{page}"
            response = session.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            category_content = soup.find('div', {'class': 'category_content centerindent for-this'})

            if not category_content:
                url = f"{base_url}/categories/{category}/{page}"
                response = session.get(url)
                soup = BeautifulSoup(response.content, "html.parser")
                category_content = soup.find('div', {'class': 'category_content centerindent for-this'})

            if category_content:
                for a in category_content.findAll('a', {'class': 'day'}):
                    titles.append(a.get_text(strip=True))
                    links.append(a.get('href'))

            if len(links) >= max_links_per_category:
                break

        for i, link in enumerate(links[:max_links_per_category]):
            result = session.get(link).text
            doc = BeautifulSoup(result, 'html.parser')

            # Extract image URL
            try:
                image_tag = doc.find('div', {'class': 'col-md-4 col-sm-4'}).find('img')
                image_url = base_url + image_tag['src'].replace('../..', '')
                rimage = session.get(image_url).content  # Fetch image data
            except (AttributeError, IndexError, requests.exceptions.RequestException) as e:
                print(f"Error! Failed to fetch image: {e}")
                rimage = None

            # Extract other details
            try:
                rtitle = doc.find('h1', {'class': 'red'}).text.strip()
                ringredients = doc.find('div', {'class': 'col-md-12 for-padding-col'}).find_all('p')[0].text.strip()
                rservings = doc.find('div', {'class': 'times'}).findAll('div', {'class': 'times_tab'})[1].find('div', {'class': 'f12 f12'}).text.strip()
                rinstructions = doc.find('div', {'class': 'col-md-12 for-padding-col'}).find_all('p')[1].text.strip()
            except AttributeError as e:
                print(f"Failed to find recipe details: {e}")
                continue

            print(f'images: {image_url}')
            try:
                DATABASE_URL = os.environ['DATABASE_URL']
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            except Exception as e:
                conn = psycopg2.connect(
                    host="localhost",
                    database="flavors_api",
                    user=os.environ['PGUSER'],
                    password=os.environ['PGPASSWORD']
                )
                print(f"Failed to connect to database: {e}")
                continue

            try:
                cur = conn.cursor()
                query = '''INSERT INTO recipes(title, ingredients, servings, instructions, image, recipe_category) 
                           VALUES(%s, %s, %s, %s, %s, %s)'''
                record_to_insert = (
                    rtitle, ringredients, rservings, rinstructions, psycopg2.Binary(rimage) if rimage else None, category
                )
                cur.execute(query, record_to_insert)
                conn.commit()
                cur.close()
            except Exception as e:
                print(f"Failed to insert data: {e}")
                conn.rollback()

        conn.close()

except Exception as e:
    print(f"Failed to establish a new connection: {e}")
finally:
    session.close()  # Close the session after completing the task



def get_daily_recipe(conn):
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Get the current date
    today = datetime.date.today()

    # Check if a recipe has already been selected today
    cur.execute("SELECT recipe_id, date FROM daily_recipe WHERE date = %s;", (today,))
    result = cur.fetchone()

    if result:
        # If a recipe is already selected, fetch it
        cur.execute("SELECT * FROM recipes WHERE rep_id = %s;", (result['recipe_id'],))
        recipe = cur.fetchone()
    else:
        # Select a new random recipe
        cur.execute("SELECT rep_id FROM recipes;")
        all_recipe_ids = cur.fetchall()
        random_recipe_id = random.choice(all_recipe_ids)['rep_id']

        # Insert the new daily recipe into the database
        cur.execute("INSERT INTO daily_recipe (recipe_id, date) VALUES (%s, %s);", (random_recipe_id, today))
        conn.commit()

        # Fetch the newly selected recipe
        cur.execute("SELECT * FROM recipes WHERE rep_id = %s;", (random_recipe_id,))
        recipe = cur.fetchone()

    cur.close()
    return recipe


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
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'])

    daily_recipe = get_daily_recipe(conn)

    conn.close()

    return render_template('index.html', recipe=daily_recipe)


@app.route('/terms', methods=['GET'])
def terms():
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost",
            database="flavors_api",
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'])

    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # all_recipes = cur.execute('SELECT * FROM recipes;').fetchall()
    cur.execute('SELECT * FROM users;')
    recipes = cur.fetchall()

    return render_template('terms.html')


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    recipes = []
    if query:
        try:
            DATABASE_URL = os.environ['DATABASE_URL']
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except Exception as e:
            conn = psycopg2.connect(
                host="localhost",
                database="flavors_api",
                user=os.environ['PGUSER'],
                password=os.environ['PGPASSWORD']
            )
            print(f"Failed to connect to database: {e}")

        try:
            cur = conn.cursor()
            cur.execute("SELECT rep_id, title, ingredients, servings, instructions FROM recipes WHERE title ILIKE %s", (f'%{query}%',))
            recipes = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Failed to fetch data: {e}")
    return render_template('search.html', recipes=recipes)


@app.route('/search-image/<int:recipe_id>', methods=['GET'])
def search_image(recipe_id):
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except Exception as e:
        conn = psycopg2.connect(
            host="localhost",
            database="flavors_api",
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD']
        )
        print(f"Failed to connect to database: {e}")

    try:
        cur = conn.cursor()
        cur.execute("SELECT image FROM recipes WHERE rep_id = %s", (recipe_id,))
        image_data = cur.fetchone()[0]
        cur.close()
        conn.close()
        return send_file(io.BytesIO(image_data), mimetype='image/jpeg')
    except Exception as e:
        print(f"Failed to fetch image: {e}")
        return '', 404


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to be logged in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username:
            flash('Your username is required!')
        elif not password:
            flash('Your password is required!')
        else:
            try:
                DATABASE_URL = os.environ['DATABASE_URL']
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            except:
                conn = psycopg2.connect(
                    host="localhost",
                    database="flavors_api",
                    user=os.environ['PGUSER'],
                    password=os.environ['PGPASSWORD'])
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute('SELECT * FROM users WHERE user_handle = %s AND user_password = %s', (username, password))
            user = cur.fetchone()
            conn.close()

            if user:
                session['user_id'] = user['user_id']
                session['username'] = user['user_handle']
                session['email'] = user['email']
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password!')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html', username=session['username'], email=session['email'])


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name_user = request.form.get('user_firstname')
        email = request.form.get('email')
        username = request.form.get('user_handle')
        password = request.form.get('user_password')
        confirm_pass = request.form.get('confirm_password')

        if not name_user:
            flash('Your name is required!')
        elif not email:
            flash('Your email is required!')
        elif not username:
            flash('Your username is required!')
        elif not password:
            flash('A password is required!')
        elif password != confirm_pass:
            flash('The passwords do not match!')
        else:
            try:
                DATABASE_URL = os.environ['DATABASE_URL']
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            except:
                conn = psycopg2.connect(
                    host="localhost",
                    database="flavors_api",
                    user=os.environ['PGUSER'],
                    password=os.environ['PGPASSWORD'])
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute('INSERT INTO users (user_handle, user_password, user_firstname, email) VALUES (%s, %s, %s, %s)',
                        (username, password, name_user, email))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('email', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))



# Home screen
@app.route('/recipes/category', methods=['GET'])
def all_recipe():
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost",
            database="flavors_api",
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'])

    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Query the distinct recipe categories
    cur.execute("SELECT DISTINCT recipe_category FROM recipes")
    categorie = [row['recipe_category'] for row in cur.fetchall()]

    cur.close()
    conn.close()

    return render_template('all_recipe.html', categories=categories)


@app.route('/recipes/category/<category>')
def category_recipe(category):
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        conn = psycopg2.connect(
            host="localhost",
            database="flavors_api",
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD']
        )

    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM recipes WHERE recipe_category = %s;', (category,))
    recipes = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('category_recipe.html', recipes=recipes)


def get_recipe_id(rep_id):
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost",
            database="flavors_api",
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'])

    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM recipes WHERE rep_id = %s', (rep_id,))
    recipes = cur.fetchone()

    conn.close()
    if recipes is None:
        abort(404)
    return recipes


@app.route('/<int:rep_id>')
def recipe_id(rep_id):
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost",
            database="flavors_api",
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'])
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM recipes WHERE rep_id = %s', (rep_id,))
    recipe = cur.fetchone()
    cur.close()
    conn.close()
    if recipe is None:
        abort(404)
    return render_template('recipes.html', recipe=recipe)


@app.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        servings = request.form['servings']
        category = request.form['recipe_category']
        instructions = request.form['instructions']

        image = request.files['image']
        image_data = image.read() if image else None

        if not title:
            flash('Title is required!')
        if not ingredients:
            flash('Ingredients is required!')
        if not servings:
            flash('Servings is required!')
        if not category:
            flash('Category is required!')
        if not image:
            flash('Image is required!')
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
                    user=os.environ['PGUSER'],
                    password=os.environ['PGPASSWORD'])
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute('INSERT INTO recipes (title, ingredients, servings, instructions, image, recipe_category) VALUES (%s, %s, %s, %s, %s, %s)',
                        (title, ingredients, servings, instructions, psycopg2.Binary(image_data), category))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))

    # Fix code below, ingredients add button triggers instructions button
    ingredients = []
    # instructions = []

    ingredients = ingredients.append(ingredients)
    ingredients = request.form.get('ingredients')

    # instructions = instructions.append(instructions)
    # instructions = request.form.get('instructions')
    return render_template('create.html', ingredients=ingredients)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/flavors/api/recipes', methods=['GET'])
def api_all():
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost",
            database="flavors_api",
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD']
        )

    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM recipes;')
    all_recipes = cur.fetchall()

    # Process each recipe to convert binary image data to base64 string
    for recipe in all_recipes:
        if recipe['image']:
            recipe['image'] = base64.b64encode(recipe['image']).decode('utf-8')

    return jsonify({'recipes': all_recipes})


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

    # conn = sqlite3.connect('flavor_api_database.db')
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost",
            database="flavors_api",
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'])

    # conn.row_factory = dict_factory
    # cur = conn.cursor()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(query, to_filter)
    results = cur.fetchall()
    return jsonify(results)


# Inserted user recipe(s)
def insert_recipe(rep_id, title, ingredients, servings, instructions):
    # conn = sqlite3.connect('flavor_api_database.db')
    conn = get_db_connection()
    cur = conn.cursor()
    # cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
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
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'])

    recipes = request.get_json()

    # rep_id = request.json['rep_id']

    title = request.json['title']
    ingredients = request.json.get('ingredients', "")
    servings = request.json.get('servings', "")
    instructions = request.json.get('instructions', "")
    # conn = sqlite3.connect('flavor_api_database.db')
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # conn.execute('INSERT INTO recipes(id, title, ingredients, servings, instructions) VALUES(?, ?, ?, ?, ?)', (id, title, ingredients, servings, instructions))
    cur.execute('INSERT INTO recipes(title, ingredients, servings, instructions) VALUES(%s, %s, %s, %s);',
                (title, ingredients, servings, instructions))
    conn.commit()
    conn.close()
    return jsonify({'recipe': recipes}), 201


# Filter through recipes database
# def get_recipe_by_id(rep_id):
# conn = sqlite3.connect('flavor_api_database.db')
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
    # Old code
    # ========
    # conn = psycopg2.connect(
    # host="localhost",
    # database="flavors_api",
    # user=os.environ['DB_USERNAME'],
    # password=os.environ['DB_PASSWORD'])
    # cur = conn.cursor()
    # cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    # statement = "SELECT rep_id, title, ingredients, servings, instructions FROM recipes WHERE rep_id = ?"
    # cur.execute("SELECT rep_id, title, ingredients, servings, instructions FROM recipes WHERE rep_id = %s", [rep_id])
    # recipe = cur.fetchone()
    # recipe = get_recipe_by_id(rep_id)
    # return jsonify({'recipe': recipe}) #can change array position from 0 - 4
    # original return jsonify({'recipe': recipe})

    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost",
            database="flavors_api",
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'])

    # cur = conn.cursor()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # statement = "SELECT rep_id, title, ingredients, servings, instructions FROM recipes WHERE rep_id = ?"
    # cur.execute("SELECT rep_id, title, ingredients, servings, instructions FROM recipes WHERE title = %s", [rep_name])
    cur.execute("SELECT * FROM recipes;")
    recipes = cur.fetchall()

    # .casefold ignores case strings (Whether uppercase or lower)
    recipe = [recipe for recipe in recipes if
              rep_name.casefold() in recipe['title'].casefold() or rep_name.casefold() in recipe[
                  'ingredients'].casefold()]
    # for recipe in recipes:
    #    if rep_name in recipes:
    #        break

    return jsonify({'recipe': recipe})  # can change array position from 0 - 4
    # original return jsonify({'recipe': recipe})


# Connect to database
def get_db_connection():
    # conn = sqlite3.connect('flavor_api_database.db')
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost",
            database="flavors_api",
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'])
    # conn.row_factory = sqlite3.Row
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

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
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'])
    post = conn.execute('SELECT *FROM recipes WHERE title = %s', {'recipe': rep_name}).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


# Modify recipe
@app.route("/flavors/api/recipes/<int:rep_id>", methods=["PUT"])
def update_recipe(rep_id):
    recipes_edit = request.get_json()
    # code to update recipe in database by id (rep_id) postgresql using psycopg2.connect
    # conn = sqlite3.connect('flavor_api_database.db')

    # rep_id = request.json['rep_id']
    # title = request.json.get('title', '')
    # ingredients = request.json.get('ingredients', "")
    # servings = request.json.get('servings', "")
    # instructions = request.json.get('instructions', "")
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        db = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        db = psycopg2.connect(
            host="localhost",
            database="flavors_api",
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'])

    cursor = db.cursor()
    cursor.execute(
        "UPDATE recipes SET title = %s, ingredients = %s, servings = %s, instructions = %s WHERE rep_id = %s", (
            recipes_edit['title'], recipes_edit['ingredients'], recipes_edit['servings'], recipes_edit['instructions'],
            rep_id))

    # statement =  "UPDATE recipes SET title = %s, ingredients = %s, servings = %s, instructions = %s WHERE rep_id = %s"
    # cursor.execute(statement, [title, ingredients, servings, instructions, rep_id])
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
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'])

    cursor = db.cursor()
    statement = "DELETE FROM recipes WHERE rep_id = %s"
    cursor.execute(statement, [rep_id])
    db.commit()
    return ('Deleted'), 201


@app.route('/image/<int:id>')
def image(id):
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        conn = psycopg2.connect(
            host="localhost",
            database="flavors_api",
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'])

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
# @app.route('/flavors/api/recipes', methods=['GET', 'POST'])
# def api_recipe_request():

# from flask_httpauth import HTTPBasicAuth

# auth = HTTPBasicAuth()

# @auth.get_password
# def get_password(username):
#    if username == 'fred':
#        return 'python'
#    return None