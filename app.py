from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('mstone_result.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS mstone_result (
        name TEXT,
        gender TEXT,
        roll_number TEXT,
        total_marks INTEGER,
        imea_ii INTEGER,
        pspp INTEGER,
        dcs INTEGER,
        etw INTEGER,
        es_practical INTEGER,
        web_development INTEGER,
        pspp_practical INTEGER,
        dcs_practical INTEGER,
        etw_practical INTEGER
    )
''')




conn.commit()
conn.close()



@app.route('/')
def index():
  return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def get_result():
    if request.method == 'POST':
        roll_number = request.form['roll_number']

        try:
            # Connect to the database within the function
            conn = sqlite3.connect('mstone_result.db')
            cursor = conn.cursor()

            # Fetch data using roll number
            cursor.execute('SELECT * FROM mstone_result WHERE roll_number = ?', (roll_number,))
            result = cursor.fetchone()
            # Print the result dictionary for inspection
            print(result)

            if result:
                return render_template('result.html', result=result)
            else:
                return render_template('not_found.html'), 404  # Or a specific message in result.html

        except sqlite3.Error as e:
            return render_template('error.html', error_message=str(e))

        finally:
            conn.close()  # Ensure connection closure

    # Handle GET request (initial rendering of the form)
    return render_template('index.html')



if __name__=='__main__':
  app.run(debug=True)

