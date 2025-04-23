from flask import Flask, render_template, request, redirect, url_for, flash, session
import os,secrets
from db_manager import Database
from performance_test import *

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Current file's directory
DATABASE_FOLDER = os.path.abspath(os.path.join(BASE_DIR, 'database_files'))
app.secret_key = secrets.token_hex(16)  # needed for flash messages
loaded_db = None                         # to store currently loaded database
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/existing')
def existing_databases():
    databases = [f for f in os.listdir(DATABASE_FOLDER) if f.endswith('.pkl')]
    return render_template('existing_db.html', databases=databases)


@app.route('/load-database', methods=['POST'])
def load_database():
    #global loaded_db
    selected_db = request.form.get('selected_db')
    if selected_db:
        db_path = os.path.join(DATABASE_FOLDER, selected_db)
        loaded_db = Database.load_database(db_path)

        # ✅ Store only the name in session
        session['selected_db_name'] = selected_db

        flash(f"Database '{selected_db}' loaded successfully.", 'success')
        return redirect(url_for('dashboard'))
    else:
        flash("No database selected.", 'error')
        return redirect(url_for('existing_databases'))
    

@app.route('/create-database', methods=['POST','GET'])
def create_database():
    if request.method == 'POST':
        #global loaded_db
        db_name = request.form.get('db_name')
        if not db_name.endswith('.pkl'):
            db_name += '.pkl'

        db_path = os.path.join(DATABASE_FOLDER, db_name)

        if os.path.exists(db_path):
            flash(f"Database '{db_name}' already exists!", 'error')
            return redirect(url_for('create_database_page'))
        else:
            loaded_db = Database(db_name)

            # ✅ Store only the name in session
            session['selected_db_name'] = db_name

            loaded_db.save_database(db_path)
            flash(f"Database '{db_name}' created successfully.", 'success')
            return redirect(url_for('dashboard'))
    return render_template('create_db.html')

@app.route('/dashboard')
def dashboard():
    # if loaded_db is None:
    #     flash("No database loaded.", 'error')
    #     return redirect(url_for('home'))
    name = session.get('selected_db_name')
    if name:
        db_path = os.path.join(DATABASE_FOLDER, name)
        loaded_db = Database.load_database(db_path)

    table_names = []
    for table_name, table_obj in loaded_db.tables.items():
        table_names.append(table_name)
    return render_template('db_dashboard.html', tables= table_names, db_name = name)  

@app.route('/performance-analysis')
def performance_analysis():
    return render_template('performance_analysis.html')


@app.route('/insertion-time')
def measure_insertion_time():
    rows = request.args.get('rows', type=int)
    if not rows:
        return "Number of rows not specified!", 400

    sizes, bplus_times, brute_times = measure_insertion_performance("students","performance",rows)
    plot_performance(sizes, bplus_times, brute_times, "Insertion", "students")

    # Image URL path (for HTML)
    filename = 'performance_plots/students_insertion_times.png'
    image_url = url_for('static', filename=filename)
    return render_template('insertion_performance.html', image_url=image_url)


@app.route('/deletion-time')
def measure_deletion_time():
    rows = request.args.get('rows', type=int)
    if not rows:
        return "Number of rows not specified!", 400
    sizes, bplus_times, brute_times = measure_deletion_performance("students","performance",rows)
    plot_performance(sizes, bplus_times, brute_times, "Deletion", "students")

    # Image URL path (for HTML)

    filename = 'performance_plots/students_deletion_times.png'
    image_url = url_for('static', filename=filename)
    return render_template('deletion_performance.html', image_url = image_url)

@app.route('/searching-time')
def measure_searchingn_time():
    rows = request.args.get('rows', type=int)
    if not rows:
        return "Number of rows not specified!", 400

    sizes, bplus_times, brute_times = measure_search_performance("students","performance",rows)
    plot_performance(sizes, bplus_times, brute_times, "Search", "students")

    filename = 'performance_plots/students_search_times.png'
    image_url = url_for('static', filename=filename)
    return render_template('searching_performance.html', image_url = image_url)

@app.route('/rangequery-time')
def measure_rangequery_time():
    rows = request.args.get('rows', type=int)
    if not rows:
        return "Number of rows not specified!", 400    

    sizes, bplus_times, brute_times = measure_range_query_performance("students","performance",rows)
    plot_performance(sizes, bplus_times, brute_times, "range-query", "students")

    # Image URL path (for HTML)
    filename = 'performance_plots/students_range-query_times.png'
    image_url = url_for('static', filename=filename)
    return render_template('rangequery_performance.html', image_url = image_url)


@app.route('/create-table', methods = ['POST','GET'])
def create_table():
    if request.method == 'POST':
        table_name = request.form.get('table_name')
        columns = request.form.getlist('columns[]')
        primary_key = request.form.get('primary_key')

        db_name = session.get('selected_db_name')
        if db_name:
            db_path = os.path.join(DATABASE_FOLDER, db_name)
            loaded_db = Database.load_database(db_path)
        else:
            flash(f"No database selected...",'error')
            return redirect(url_for('dashboard'))

        print(loaded_db.tables)
        loaded_db.create_table(table_name, columns, primary_key)  # Call your method to create the table
        loaded_db.save_database(db_path)
        print(loaded_db.tables)

        # Redirect to the same page after creating the table to reload the form
        return redirect(url_for('dashboard'))

    return render_template('create_tables.html')  # This will render the form on GET request


# Delete Table
@app.route('/delete-table', methods=['POST'])
def delete_table():
    table_name = request.form.get('table_name')
    if not table_name:
        flash("Table name is required.", 'error')

    db_name = session.get('selected_db_name')
    if db_name:
        db_path = os.path.join(DATABASE_FOLDER, db_name)
        loaded_db = Database.load_database(db_path)

    loaded_db.delete_table(table_name)
    return redirect(url_for('dashboard'))


# Choose Table
@app.route('/choose-table', methods=['POST'])
def choose_table():
    table_name = request.form.get('table_name')
    if not table_name:
        flash("Table name is required.", 'error')
        return redirect(url_for('dashboard'))
    
    session['selected_table'] = table_name   # 🔥 Save selected table in session
    return redirect(url_for('table_dashboard'))

@app.route('/table-dashboard')
def table_dashboard():
    table_name = session.get('selected_table')
    if not table_name:
        flash("No table selected.", "error")
        return redirect(url_for('dashboard'))
    
    return render_template('table_dashboard.html', table_name=table_name)

@app.route('/insert-record', methods = ['POST','GET'])
def insert_record():
    if request.method == 'POST':
        table_name = session.get('selected_table')
        db_name = session.get('selected_db_name')

        if table_name and db_name:
            if db_name:
                db_path = os.path.join(DATABASE_FOLDER, db_name)
                loaded_db = Database.load_database(db_path)
        else:
            flash("Table name and database is required.", 'error')
            return redirect(url_for('dashboard'))


        row = {}
        columns = loaded_db.tables[table_name].columns
        
        for col in columns:
            value = request.form.get(col)
            row[col] = value
            
        loaded_db.insert(table_name,row)
        loaded_db.save_database(db_path)
        return redirect(url_for('table_dashboard'))

    db_name = session.get('selected_db_name')
    table_name = session.get('selected_table')
    if db_name:
        db_path = os.path.join(DATABASE_FOLDER, db_name)
        loaded_db = Database.load_database(db_path)

    columns = loaded_db.tables[table_name].columns
    return render_template('insert_record.html', table_name= table_name ,table_columns = columns)

@app.route('/update-record', methods = ['POST','GET'])
def update_record():
    if request.method == 'POST':
        table_name = session.get('selected_table')
        db_name = session.get('selected_db_name')

        if table_name and db_name:
            db_path = os.path.join(DATABASE_FOLDER, db_name)
            loaded_db = Database.load_database(db_path)
        else:
            flash("Table name and database is required.", 'error')
            return redirect(url_for('dashboard'))

        row = {}
        columns = loaded_db.tables[table_name].columns
        
        for col in columns:
            value = request.form.get(col)
            row[col] = value

            key = row['id']
            loaded_db.update("students",key,row)
            loaded_db.save_database(db_path)
            return redirect(url_for('table_dashboard'))

    db_name = session.get('selected_db_name')
    table_name = session.get('selected_table')
    if db_name:
        db_path = os.path.join(DATABASE_FOLDER, db_name)
        loaded_db = Database.load_database(db_path)

    columns = loaded_db.tables[table_name].columns
    return render_template('update_record.html', table_name= table_name ,table_columns = columns)

@app.route('/search-record', methods=['POST', 'GET'])
def search_record():
    if request.method == 'POST':
        table_name = session.get('selected_table')
        db_name = session.get('selected_db_name')

        if table_name and db_name:
            db_path = os.path.join(DATABASE_FOLDER, db_name)
            loaded_db = Database.load_database(db_path)
        else:
            flash("Table name and database are required.", 'error')
            return redirect(url_for('dashboard'))

        columns = loaded_db.tables[table_name].columns
        key = request.form.get('student_id')
        
        # Search for the record
        results = loaded_db.search(table_name, key)  # Assuming 'search' returns matching records
        return render_template('search_record.html', table_name=table_name, table_columns=columns, results=results)
    
    db_name = session.get('selected_db_name')
    table_name = session.get('selected_table')
    if db_name:
        db_path = os.path.join(DATABASE_FOLDER, db_name)
        loaded_db = Database.load_database(db_path)

    columns = loaded_db.tables[table_name].columns
    return render_template('search_record.html', table_name=table_name, table_columns=columns)

@app.route('/display-all-record')
def display_all_records():
    table_name = session.get('selected_table')
    db_name = session.get('selected_db_name')

    if db_name:
        db_path = os.path.join(DATABASE_FOLDER, db_name)
        loaded_db = Database.load_database(db_path)

        # Get records and column names
        records_dict = loaded_db.print_records(table_name)
        columns = loaded_db.tables[table_name].columns

        # Convert dict-of-dicts → list-of-dicts for Jinja rendering
        record_list = list(records_dict.values())

        return render_template(
            'display_all_record.html',
            table_name=table_name,
            records=record_list,
            table_columns=columns
        )
    else:
        return "No database selected", 400



@app.route('/delete-record', methods=['POST', 'GET'])
def delete_record():
    if request.method == 'POST':
        table_name = session.get('selected_table')
        db_name = session.get('selected_db_name')

        if table_name and db_name:
            db_path = os.path.join(DATABASE_FOLDER, db_name)
            loaded_db = Database.load_database(db_path)
        else:
            flash("Table name and database are required.", 'error')
            return redirect(url_for('dashboard'))

        key = request.form.get('student_id')

        if not key:
            flash("Primary key value is required to delete a record.", 'error')
            return redirect(url_for('delete_record'))

        loaded_db.delete(table_name, key)
        loaded_db.save_database(db_path)
        flash("Record deleted successfully!", 'success')
        return redirect(url_for('table_dashboard'))

    # For GET: show the form
    db_name = session.get('selected_db_name')
    table_name = session.get('selected_table')

    if db_name and table_name:
        db_path = os.path.join(DATABASE_FOLDER, db_name)
        loaded_db = Database.load_database(db_path)
        table_columns = loaded_db.tables[table_name].columns
        return render_template('delete_record.html', table_name=table_name, columns=table_columns)

    flash("Table and database must be selected.", 'error')
    return redirect(url_for('dashboard'))

@app.route('/range-query', methods=['POST', 'GET'])
def range_query():
    if request.method == 'POST':
        table_name = session.get('selected_table')
        db_name = session.get('selected_db_name')

        if table_name and db_name:
            db_path = os.path.join(DATABASE_FOLDER, db_name)
            loaded_db = Database.load_database(db_path)
        else:
            flash("Table name and database are required.", 'error')
            return redirect(url_for('dashboard'))

        Min_value= request.form.get('min_value')
        Max_value= request.form.get('max_value')

        if not Min_value or not Max_value:
            flash(" Values are required to range query.", 'error')
            return redirect(url_for('range_query'))

        results = loaded_db.range_query(table_name,Min_value, Max_value)
        columns = loaded_db.tables[table_name].columns
        
        flash("Records returned successfully!", 'success')
        return render_template('range_query_results.html', results=results, columns=columns)

    # For GET: show the form
    db_name = session.get('selected_db_name')
    table_name = session.get('selected_table')

    if db_name and table_name:
        db_path = os.path.join(DATABASE_FOLDER, db_name)
        loaded_db = Database.load_database(db_path)
        table_columns = loaded_db.tables[table_name].columns
        return render_template('range_query.html', table_name=table_name, columns=table_columns)

    flash("Table and database must be selected.", 'error')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    if not os.path.exists(DATABASE_FOLDER):
        os.makedirs(DATABASE_FOLDER)
    app.run(debug=True)
