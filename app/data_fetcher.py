from neo4j.v1 import GraphDatabase
from pprint import pprint


class Fetcher:
    def __init__(self):
        self.data = None
        self.games = None
        self.moves = None

        self.tags = ['White', 'Black', 'Date', 'HalfMoves', 'Moves', 'Result',
                     'WhiteElo', 'BlackElo', 'GameNumber', 'Event', 'Site',
                     'EventDate', 'Round', 'ECO', 'Opening']

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

        :return:
        """
        games = list()
        moves = list()
        game_list = None
        for game in self.data:
            for row in game:
                print('Row: {}'.format(row))
                game_list = list()
                tag = row.split(':')[0]
                if tag in self.tags:
                    game_list.append(row)
                break
            break

            games.append(game_list)

        self.games = games

    def establish_connection(self):
        pass

    def insert_data(self):
        pass

    @staticmethod
    def print_friends_of(name, driver):
        with driver.session() as session:
            with session.begin_transaction() as tx:
                for record in tx.run("MATCH (a:Person)-[:KNOWS]->(f) "
                                     "WHERE a.name = {name} "
                                     "RETURN f.name", name=name):
                    print(record["f.name"])


if __name__ == '__main__':
    path = '/Users/aggelikiromanou/Desktop/MSDS/5_Data_mining/Assignment_2/' \
           'chess-games-and-positions-graph-model/data/chessData.txt'

    fetcher = Fetcher()
    fetcher.read_from_file(path)

    pprint(fetcher.data[0])
    fetcher.split_into_two_datasets()
    pprint(fetcher.games)


    # uri = 'bolt://localhost:7687'
    #
    # driver = GraphDatabase.driver(uri, auth=("neo4j", "Aggelikh1992"))
    #
    # Fetcher.print_friends_of("Alice", driver)
