
from mysql.connector import MySQLConnection, Error
import mysql.connector
import json
from flask import Response, request, jsonify
from flask import Flask


from Database import DatabaseConfig as Database

from IPython import embed

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
        print("ERROR: ", e)

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
        print("ERROR: ", e)

    finally:
        cursor.close()
        cnx.close()



# TO DO
# @app.route('/category/update', methods=['POST'])
# def updateCategory():

# TO DO
# @app.route('/category/add', methods=['POST'])
# def addCategory():


# TO DO
# @app.route('/category/delete/<category>')
# def deleteCategory(category):
#         try:
#         cnx = mysql.connector.connect(user= Database['user'],
#                                 password=Database['password'],
#                                 host= Database['host'],
#                                 database=Database['database']
#         )
#         cursor = cnx.cursor()
        
#         #Check user category parameter is valid:
#         cursor.callproc('getCategories')
#         for result in cursor.stored_results():
#             data = (result.fetchall())
#         isCatValid = False
#         for d in data:
#             if (d[0] == category ): 
#                 isCatValid = True
#                 break
#         if not (isCatValid): return jsonify("Cannot find the category to delete it!")

#         #cat parameter is valid, continue.
#         args = [category]
        

#         resp = jsonify("Successfuly delete the category and all the recipes under the category.")
#         resp.status_code = 200
#         return resp

#     except Error as e:
#         print("ERROR: ", e)

#     finally:
#         cursor.close()
#         cnx.close()



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
        print("ERROR: ", e)

    finally:
        cursor.close()
        cnx.close()

@app.route("/recipe-details/<int:id>")
def getRecipeDetails(id):
    try:
        # # return an empty string if id is not an integer.
        # if not (isinstance(id, int)): 
        #     return jsonify([])

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
        print("ERROR: ", e)

    finally:
        cursor.close()
        cnx.close()

@app.route('/recipe/update', methods=['POST'])
def updateRecipe():
    try:
        content = request.get_json()
        _id = content['id']
        _category = content['category']
        _title = content['title']
        _ingredients = content['ingredients']
        _instructions = content['instructions']
        
        # _id = int (request.args.get('id'))
        # _category = request.args.get('category')
        # _title = request.args.get ('title')
        # _ingredients = request.args.get('ingredients')
        # _instructions = request.args.get('instructions')
        
        cnx = mysql.connector.connect(user= Database['user'],
                                password=Database['password'],
                                host= Database['host'],
                                database=Database['database']
            )
        cursor = cnx.cursor()
        # validate the received values
        # print ("**********", _id, _category, _title, _ingredients, _instructions)
        if (_id and _category and _title and _ingredients and _ingredients and request.method == 'POST' ):
            # save edits
            args = [_id, _category, _title, _ingredients, _instructions]
            cursor.callproc('UpdateRecipeDetails', args)
            cnx.commit()
            resp = jsonify('Successfully updated the recipe!')
            resp.status_code = 200
            return resp
        else:
            return not_found()

    except Error as e:
        print("ERROR: " , e)
        
    finally:
        cursor.close()
        cnx.close()

@app.route('/recipe-details/add', methods=['POST'])
def addRecipe():
    try:
        content = request.get_json()
        id = content['id']
        category = content['category']
        title = content['title']
        ingredients = content['ingredients']
        instructions = content['instructions']
        
        cnx = mysql.connector.connect(user= Database['user'],
                                password=Database['password'],
                                host= Database['host'],
                                database=Database['database']
            )
        cursor = cnx.cursor()
        # validate the received values
        if (id and category and title and ingredients and ingredients and request.method == 'POST' ):
            # save edits
            args = [id, category, title, ingredients, instructions]
            cursor.callproc('addRecipe', args)
            cnx.commit()
            resp = jsonify('Successfully added one recipe!')
            resp.status_code = 200
            return resp
        else:
            return not_found()

    except Error as e:
        print("ERROR: " , e)
    finally:
        cursor.close()
        cnx.close()

@app.route('/recipe-details/delete/<int:id>')
def deleteRecipe(id):
    try:
        cnx = mysql.connector.connect(user= Database['user'],
            password=Database['password'],
            host= Database['host'],
            database=Database['database']
        )
        cursor = cnx.cursor()
        args = [id]
        cursor.callproc('deleteRecipe', args)
        cnx.commit()
        resp = jsonify('Successfully deleted the recipe!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print("ERROR: ", e)
    finally:
        cursor.close() 
        cnx.close()





@app.errorhandler(404)
def not_found(error=None):
    message = [{
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }]
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == '__main__':
    app.run(debug=True)