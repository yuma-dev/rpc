from io import UnsupportedOperation
from unicodedata import normalize
import json

def write(game, time):
    if isinstance(game, str) and isinstance(time, int):

        game = normalize('NFC', game)

        finished = False

        with open("data/database.json", "r") as f:
            oldData = json.load(f)



        try:

            with open("data/database.json", "r") as f:
                data = json.load(f)


            if game in data[0]:

                seconds = data[0][game] 
                data[0][game] = seconds + time

            else:

                data[0][game] = time

            finished = True


        except Exception as e:
            finished = False
            with open("data/database.json", "w") as f:
                json.dump(oldData, f, indent=4,sort_keys=True)
            print('exception')
            raise Exception(e)



        if finished:

            with open("data/database.json", "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=4,sort_keys=True)

            print('finished')

    else:
        return UnsupportedOperation

def read(game):

    game = normalize('NFC', game)


    with open("data/database.json", 'r') as f:

        print(f)
        data = json.load(f)

        if game in data[0]:

            seconds = data[0][game]
            return seconds

        else:
            return None


