
from mysql.connector import MySQLConnection, Error
import mysql.connector
import json
from flask import Response, request, jsonify
from flask import Flask


from Database import DatabaseConfig as Database

# from IPython import embed

app = Flask(__name__)

import platform
if (platform.system() == 'Windows'):
    from flask_cors import CORS
    CORS(app)
    print ("Windows detected, enabling CORS")

@app.route("/category")
def getCategories():
    try:
        cnx = mysql.connector.connect(user= Database['user'],
                                password=Database['password'],
                                host= Database['host'],
                                database=Database['database']
        )
        cursor = cnx.cursor()

        cursor.callproc('getCategories')
        for result in cursor.stored_results():
            data = (result.fetchall())  # data is a list of tuples [('BLW',"Baby lead weaning"), ('SMOOTHIE',"Smoothies")]

        retVal = []
        for d in data:  #d is a tuple - example: ('SMOOTHIE',"Smoothies")
            retVal +=[{'title' : d[1], 'category':d[0]}]  

        resp = jsonify(retVal)
        resp.status_code = 200
        return resp

    except Error as e:
        print(e)

    finally:
        cursor.close()
        cnx.close()


@app.route("/category/<cat>")
def getOneCategory(cat):
    try:
        cnx = mysql.connector.connect(user= Database['user'],
                                password=Database['password'],
                                host= Database['host'],
                                database=Database['database']
        )
        cursor = cnx.cursor()
        cursor.callproc('getCategories')
        
        # args = [cat]
        # cursor.callproc('getCategoryTitle', args)
        for result in cursor.stored_results():
            data = (result.fetchall())  # data is a list of tuples [('BLW',"Baby lead weaning"), ('SMOOTHIE',"Smoothies")]

        retVal = []
        for d in data:  #d is a tuple - example: ('SMOOTHIE',"Smoothies")
            if (d[0] == cat ):
                retVal +=[{'category':d[0], 'title' : d[1]}]

        resp = jsonify(retVal)
        resp.status_code = 200
        return resp

    except Error as e:
        print(e)

    finally:
        cursor.close()
        cnx.close()

@app.route("/recipes-list/<category>")
def getRecipesList(category):
    try:
        cnx = mysql.connector.connect(user= Database['user'],
                                password=Database['password'],
                                host= Database['host'],
                                database=Database['database']
        )
        cursor = cnx.cursor()
        
        #Check user category parameter is valid:
        cursor.callproc('getCategories')
        for result in cursor.stored_results():
            data = (result.fetchall())
        isCatValid = False
        for d in data:
            if (d[0] == category ): 
                isCatValid = True
                break
        if not (isCatValid): return jsonify([])

        #cat parameter is valid, continue.
        args = [category]
        cursor.callproc('getRecipesTitle', args)
        for result in cursor.stored_results():
            data = (result.fetchall())   

        retVal = []
        for d in data:
            retVal +=[{'id' : d[0], 'title':d[1]}]  

        resp = jsonify(retVal)
        resp.status_code = 200
        return resp

    except Error as e:
        print(e)

    finally:
        cursor.close()
        cnx.close()

    


@app.route("/recipe-details/<int:id>")
def getRecipeDetails(id):
    try:
        cnx = mysql.connector.connect(user= Database['user'],
                                password=Database['password'],
                                host= Database['host'],
                                database=Database['database']
        )
        cursor = cnx.cursor()

        args = [id]
        cursor.callproc('getRecipeDetails', args)
        for result in cursor.stored_results():
            data = (result.fetchall())   

        retVal = []
        for d in data:
            retVal +=[{'id' : d[0],
             'category':d[1],
             'title': d[2] ,
             'ingredients': d[3],
             'instructions': d[4]
                # TO DO: add note and iconUrls 
                #Make sure modify front-end side: recipe.ts 
             }]  

        resp = jsonify(retVal)
        resp.status_code = 200
        return resp

    except Error as e:
        print(e)

    finally:
        cursor.close()
        cnx.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == '__main__':
    app.run(debug=True)