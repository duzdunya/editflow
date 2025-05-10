Editflow is a Python library that serves as an extension toolkit for moviepy, enriching its feature set. 

This library provides a general template system for videos with advanced capabilities like relative time management, grid systems, easing functions, and animations. 
It is designed as a hierarchical container system organized in the following order: Screen, Film, Tape, and Sound.

### example usage
```Python
from editflow import Tape, Film, Screen
import moviepy as mp

screen = Screen()
film = Film()
box = mp.ImageClip("./box.png", duration=3)
boxtape1 = Tape(box)
boxtape2 = Tape(box)
film.add_tape(boxtape1, pos=(6,6), offset=(1,1))
film.add_tape(boxtape2, pos=(0,11), anchor="topright")
screen.add_film(film)
screen.compose()
screen.render("test.mp4")
```
![info](https://github.com/user-attachments/assets/874e62e2-fc66-4517-b54c-20f13918d266)
