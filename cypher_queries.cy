//Query 1 
MATCH (game:Game)-[r:Move]->(position {fen: 'r1bqkbnrpppp1ppp2n51B2p34P35N2PPPP1PPPRNBQK2R'})
WITH count(*) as total_games
MATCH (game:Game)-[r:Move]->(position {fen: 'r1bqkbnrpppp1ppp2n51B2p34P35N2PPPP1PPPRNBQK2R'})
WHERE game.result = 'White'
WITH count(*) as white_result, total_games
RETURN 100.0 * white_result / total_games as percentage_of_white_wins

//Query 2
MATCH (game:Game)-[r:Move]->(position {fen: 'r1bqkbnrpppp1ppp2n51B2p34P35N2PPPP1PPPRNBQK2R'})
RETURN COUNT(game.gameId) AS numberOfGames, game.result

//Query 3
MATCH (tournament:Tournament)
MATCH (game:Game)<-[r:Include]-(tournament)
WITH count(game.gameId) as numberOfGames, collect(game.gameId) as gamesIds,  tournament.name as tournament ORDER BY numberOfGames DESC
MATCH (player:Player)-[r:Plays]->(game:Game)
WHERE player.name ='Karpov  Anatoly' and game.gameId in gamesIds
RETURN  count(player.name) as NumberOfPlayerGames, tournament, numberOfGames LIMIT 1

//Query 4
MATCH (game:Game)<-[r:Opening]-(openMove:OpenMove {name: 'Ruy Lopez'})
WITH COLLECT(game.gameId) AS gamesIds
MATCH (player:Player)-[r:Plays]->(game:Game)
WHERE game.gameId IN gamesIds
RETURN player.name, count(*) as games_num
ORDER BY games_num DESC LIMIT 1

//Query 6
MATCH (game)-[r:Move]->(position:Position)
MATCH (player:Player)-[:Plays]->(game)
WITH game as current, tournament as tournamentGame, player as Players, r.moveName as MovesName, toInt(r.moveId) as MovesId Order by MovesId
RETURN  COLLECT(DISTINCT MovesName) as Moves, current.result as GameResult, current.date as GameDate, current.moves as NumberOfMoves, tournamentGame.name as Tournament, collect(DISTINCT Players.name) as Players