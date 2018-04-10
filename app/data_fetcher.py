from neo4j.v1 import GraphDatabase
from pprint import pprint
import re


class Fetcher:
    def __init__(self):
        self.data = None
        self.games = list()
        self.moves = list()

        self.game_tags = ['White', 'Black', 'Date', 'HalfMoves', 'Moves', 'Result',
                          'WhiteElo', 'BlackElo', 'GameNumber', 'Event', 'Site',
                          'EventDate', 'Round', 'ECO', 'Opening']

        self.move_tags = ['MoveNumber', 'Side', 'Move', 'FEN', 'GameNumber']

    def read_from_file(self, path):
        """
        Read file from path nd store in a list of lists object's variable.
        :param path: str. with the path of the file
        """
        with open(path, 'r', encoding='utf8') as f:
            data = f.read().split('=' * 27 + ' Game ' + '=' * 31 + '=' * 23)

        processed_data = list()
        for row in data:
            if row:
                processed_data.append(row.split('\n'))

        self.data = processed_data

    def split_into_two_datasets(self):
        """
        Parses the input data file and creates two lists with the data from the games
        and the data from the moves of each game.
        """
        games = list()
        moves = list()
        for game in self.data:
            game_list = list()
            for row in game:
                tag = row.split(':')[0]

                # extract game stats
                if tag in self.game_tags:
                    game_list.append(row.split(': ')[1])

                # extract move stats
                if 'MoveNumber' in str(row):
                    row_list = list()
                    for element in row.split(',  '):
                        row_list.append(element.split(': ')[1])

                    moves.append(row_list)
            games.append(game_list)

        self.games = games
        self.moves = moves

    @staticmethod
    def create_string_from_list(elements_list):
        """
        Concatenates the elements of a list into onw string separated by commas.
        :param elements_list: list, that needs to be concatenated
        :return: str, of input list's elements separated by commas
        """
        elements_string = ''
        for i in elements_list:
            elements_string += str(i) + ","
        elements_string = elements_string[:-1]

        return elements_string

    def write_to_csv(self, file1, file2):
        """
        Writes the objects lists into two .csv files
        :param file1: str file path to be writen
        :param file2: str file path to be writen
        """
        with open(file1, 'w', encoding='utf8') as f:
            f.write('{}\n'.format(self.create_string_from_list(self.game_tags)))
            for game in self.games:
                f.write('{}\n'.format(self.create_string_from_list(game)))

        with open(file2, 'w', encoding='utf8') as f:
            f.write('{}\n'.format(self.create_string_from_list(self.move_tags)))
            for move in self.moves:
                f.write('{}\n'.format(self.create_string_from_list(move)))

    @staticmethod
    def establish_connection():
        """
        Establishes a connection with neo4j
        :return: neo4j instance for the given URI and configuration
        """
        uri = 'bolt://localhost:7687'
        driver = GraphDatabase.driver(uri, auth=("neo4j", "*****"))

        return driver

    @staticmethod
    def create_schema(driver):
        """
        Creates the node constraints on the graph
        :param driver: neo4j instance for the given URI and configuration
        """
        with driver.session() as session:
            with session.begin_transaction() as tx:
                tx.run("CREATE CONSTRAINT ON (game:Game) ASSERT game.gameId IS UNIQUE")
                tx.run("CREATE CONSTRAINT ON (eco:ECO) ASSERT eco.code IS UNIQUE")
                tx.run("CREATE CONSTRAINT ON (tournament:Tournament) ASSERT tournament.name IS UNIQUE")
                tx.run("CREATE CONSTRAINT ON (player:Player) ASSERT player.name IS UNIQUE")

    def insert_data_to_neo4j(self, driver, path):
        """
        Inserts data into neo4j to fill the graph.
        :param driver: neo4j instance for the given URI and configuration
        :param path: str the file path that stores the data
        """

        strg = 'LOAD CSV WITH HEADERS FROM "{}" AS row MERGE (game:Game { gameId: row.GameNumber }) ' \
               'ON CREATE SET game.gameId = row.GameNumber,game.date=row.Date,game.result=row.Result,' \
               'game.whiteElo=row.WhiteElo,game.blackElo=row.BlackElo,game.halfMoves=row.HalfMoves,game.moves=row.Moves'

        with driver.session() as session:
            with session.begin_transaction() as tx:
                tx.run(strg.format(path))


if __name__ == '__main__':
    home_path = '/Users/aggelikiromanou/Desktop/MSDS/5_Data_mining/Assignment_2/chess-games-and-positions-graph-model/data/'

    files = 'chessData.txt'
    games_file = 'games.csv'
    moves_file = 'moves.csv'

    # data pre-processing
    fetcher = Fetcher()
    fetcher.read_from_file(home_path + files)
    # pprint(fetcher.data[0])
    fetcher.split_into_two_datasets()
    fetcher.write_to_csv(home_path + games_file, home_path + moves_file)

    # neo4j
    # neo_driver = Fetcher.establish_connection()
    # fetcher.insert_data_to_neo4j(neo_driver, home_path + games_file)

