import requests, chess
from time import sleep
from stockfish import Stockfish


def getbookmoves(fen, moves, profundidad):
    global porcentaje
    if profundidad <= 0:
        print("fin linea")
    else:
        params = (
            ('variant', 'standard'),
            ('recentGames', 0),
            ('topGames', 0),
            ('moves', moves),
            ('speeds[]', ['blitz', 'rapid', 'classical']),
            ('ratings[]', ['2200', '2500']),
            ('fen', fen),
        )
        response = requests.get('https://explorer.lichess.ovh/lichess', params=params)
        parsed = response.json()
        for i in range(0, moves):
            try:
                if parsed["moves"][i]["white"] + parsed["moves"][i]["black"] + parsed["moves"][i]["draws"] / parsed["moves"][0]["white"] + parsed["moves"][0]["black"] + parsed["moves"][0]["draws"] >= porcentaje:
                    stockfish.set_fen_position(fen)
                    val_ant = stockfish.get_evaluation()['value']/100
                    stockfish.make_moves_from_current_position([parsed["moves"][i]["uci"]])
                    val_act = stockfish.get_evaluation()['value']/100
                    is_incorrect = val_act - val_ant <= 0.7
                    if is_incorrect:
                        board = chess.Board(fen)
                        board.push_san(parsed["moves"][i]["san"])
                        stockfish.set_fen_position(board.fen())
                        a = stockfish.get_best_move()
                        print({
                            'cmove': a,
                            'fen': board.fen(),
                            'san': parsed["moves"][i]["san"]
                        })
                        profundidad -= 1
                        getbookmoves(board.fen(), moves, profundidad)
            except:
                pass
            sleep(0.1)


stockfish = Stockfish("stockfish.exe")
stockfish.set_skill_level(20)
stockfish.set_depth(13)
stockfish.set_elo_rating(3500)

fen = "rnbqkbnr/pp2pppp/3p4/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1"
moves = 5
profundidad = 10
porcentaje = 0.1

getbookmoves(fen, moves, profundidad)
