# Backend Flask API for recipe site. 

This repository is a Flask REST API that retrives data from MySQL database using the MySQL.Connector driver. It's purpose is to supply content for [recipe-site-frontend](https://github.com/golnazir/recipe-site-frontend).
Currently it implements four api endpoints that return data in JSON format. These are:


* **/api/category** : returns a list of all categories in database for homepage.

* **/api/category/&lt;cat&gt;** : returns the category details for requested category. Input parameter cat must be string.
 
* **/api/recipes-list/&lt;cat&gt;** : return a list of all recipes for requested category. Input parameter cat must be string.
  
* **/api/recipe-details/&lt;id&gt;** : returns the ingredients/instructions for requested recipe.  Input parameter id must be integer.
