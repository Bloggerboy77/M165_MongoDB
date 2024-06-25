from pymongo import MongoClient

connection_string = "mongodb://localhost:27017"

client = MongoClient(connection_string)

gamedb = client.spiele

pcgames_coll = gamedb.pcgames

games = [
    {
    "game_id":"FN",
    "Titel": "Fortnite", 
    "Ausgabejahr":2017,
    "Downloadzahlen":400000000,
    "Altersgrenze":12,
    "Art":["Survival", "Battle Royale"],
    "Wertung von 1-10":8 
} , 

{
    "game_id":"MN",
    "Titel": "Minecraft", 
    "Ausgabejahr":2011,
    "Downloadzahlen":93000000,
    "Altersgrenze":7,
    "Art":["Sandbox"],
    "Wertung von 1-10":9 
},

{
    "game_id":"GTA",
    "Titel": "Grand Theft Auto V", 
    "Ausgabejahr":2013,
    "Downloadzahlen":17200000,
    "Altersgrenze":18,
    "Art":["Action-Adventure", "Open-World"],
    "Wertung von 1-10":10 
},

{
    "game_id":"BS",
    "Titel": "Bus Simulator 18", 
    "Ausgabejahr":2018,
    "Downloadzahlen":10000000,
    "Altersgrenze":10,
    "Art":["Simulator"],
    "Wertung von 1-10":7 
},

{
    "game_id":"MFS",
    "Titel": "Microsoft Flight Simulator", 
    "Ausgabejahr":2020,
    "Downloadzahlen":100000000,
    "Altersgrenze":10,
    "Art":["Flugsimulation"],
    "Wertung von 1-10":8 
},

{
    "game_id":"Spm",
    "Titel": "Marvel's Spider-Man", 
    "Ausgabejahr":2018,
    "Downloadzahlen":1000000,
    "Altersgrenze":13,
    "Art":["Action-Adventure"],
    "Wertung von 1-10":8 
},

{
    "game_id":"CS",
    "Titel": "Counter-Strike: Global Offensive", 
    "Ausgabejahr":2012,
    "Downloadzahlen":25000000, 
    "Altersgrenze":17,
    "Art":["Taktischer Ego_Shooter"],
    "Wertung von 1-10":8
},

{
    "game_id":"COD",
    "Titel": "Call  of Duty Modern Warfare", 
    "Ausgabejahr":2019,
    "Downloadzahlen":100000000,
    "Altersgrenze":18,
    "Art":["Ego-Shooter"],
    "Wertung von 1-10":9 
},

{
    "game_id":"PUBG",
    "Titel": "PUBG Mobile", 
    "Ausgabejahr":2018,
    "Downloadzahlen":1000000000,
    "Altersgrenze":16,
    "Art":["Battle Royale"],
    "Wertung von 1-10":8 
}, 

{
    "game_id":"GT",
    "Titel": "Gran Turismo Sport", 
    "Ausgabejahr":2017,
    "Downloadzahlen":10000000,
    "Altersgrenze":7,
    "Art":["Rennsimulation"],
    "Wertung von 1-10":7 
} 

]


inserts = pcgames_coll.insert_many(games)

game_ids = inserts.inserted_ids

print("# of documents inserted: " + str(len(game_ids)))
print(f"_ids of inserted games: {game_ids}")


client.close()









