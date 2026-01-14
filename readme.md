Clement Elodie 3IABD-A





///////
# Récuperation abse de données 
-curl -o /tmp/data.json https://data.atontour.info/books.json
source venv/bin/
# le port : port interne
mongoimport --uri "mongodb://localhost:27017" --db packt --collection books --file /tmp/data.json --jsonArray


docker cp data/arbres.json arbres:/tmp/arbres.json

docker exec arbres mongoimport --db arbres --collection arbres --file /tmp/arbres.json --jsonArray

# Import des arbres remarquables
mongoimport --uri "mongodb://localhost:27019" --db arbres --collection arbres --file data/arbres.json --jsonArray

# permet de lancer mongosh directement
mongosh
mongosh "mongodb://localhost:27019"


pip freeze > requirements.txt

-use packt
-db.books.find()
-db.arbres.findOne()



