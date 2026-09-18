

# termchess v2

Termchess is a chess engine hand coded in  Python.
It does the following :
- Allows to run  chess games from any position
- Loads and exports the board as FEN



https://github.com/user-attachments/assets/e45e2e6c-3e96-4248-bcb1-426a862d48a0


## Run
Uses Python 3.10 or newer

```
pip install -r requirements.txt
python -m modules.game
```

`q` and `exit` to stop it 
`forward` and `backwards` t scroll through the played moves. 
`load` reads a FEN and `export` prints one.
Everything else is read as a chess move like `a4`.

## Tests
```
pytest
```


## Why
This is not meant to replace/change any chess engine.
Its a project to learn/improve python its supposed to be improved  by adopting more
complex python/coding rules/conventions later on.

## AI Usage
AI hasnt been used to write any code. It was used to make sure that I dont implement/build bad or not future proff decisions and for the writting of the test cases.

## Quality
The quality is assured with the test cases perft 1/2/3/4 run and also  kiwipete 1/2/3

## Next Possible Features/Improvement
- a better cli
- better performane
- puzzle mode
- pgn replay



