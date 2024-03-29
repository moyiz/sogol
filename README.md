![](https://github.com/moyiz/sogol/actions/workflows/test.yml/badge.svg)
![](https://github.com/moyiz/sogol/actions/workflows/lint.yml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) 

# SOGOL
_Sound of Game of Life_ is a variation of _Conway's Game of Life_ that synthesizes each generation instead of visualizing in any UI.

## Contents
- [Installation](#installation)
- [Usage](#usage)
- [Motivation](#motivation)
- [Contributing](#contributing)
- [License](#license)
- [Version](#version)

## Installation

### Suggested: `poetry`
This is currently the recommended way. [`poetry`](https://github.com/python-poetry/poetry) will create a virtual environment and install the required dependencies and root package.
```sh
$ git clone https://github.com/moyiz/sogol.git && cd sogol
$ poetry install
$ poetry run sogol
```

### Local `pip`
```sh
$ git clone https://github.com/moyiz/sogol.git && cd sogol
$ pip install .
$ sogol
```

## Usage
By default, it will randomly generate up to 7 cells within a 3x3 matrix, and play each generation with a delay of 0.5 seconds. 
```
Sound of Game of Life.
Listen to an audio interpretation of each generation.

Usage:
    sogol [--max-column=X] [--max-row=Y] [--cells=N] [-d DELAY] [-w WAVE]
    sogol (--from-lexicon=PATH|--from-json=PATH) [-d DELAY] [-w WAVE]

Options:
    -x NUM, --max-column=NUM  Maximum column of randomly generated cells [default: 3]
    -y NUM, --max-row=NUM     Maximum row of randomly generated cells [default: 3]
    -c CELLS, --cells=CELLS   Maximum number of cells to randomly generate [default: 7]
    --from-json=PATH          Load a JSON file or stdin (-)
    --from-lexicon=PATH       Load a lexicon formatted file or stdin (-)
    -d DELAY, --delay=DELAY   Delay in seconds between each generation [default: 0.5]
    -w (sine|square|sawtooth) Select a wave to generate [default: sine]
```

## Life Lexicon
`sogol` supports loading patterns in [Life Lexicon](https://conwaylife.com/ref/lexicon/lex.htm) format. The notations are:
*  `.` (_dot_) - empty cell.
* `O` (_lower_ or _capital_) or `*` (_asterik_) - living cell.

For example, to load the [_R2D2_](https://conwaylife.com/ref/lexicon/lex_r.htm) pattern:
```bash
sogol --from-lexicon - << EOF
	.....O.....
	....O.O....
	...O.O.O...
	...O.O.O...
	OO.O...O.OO
	OO.O...O.OO
	...O...O...
	...O.O.O...
	....O.O....
	.....O.....
EOF
```

Or the [_Sidewalk_](https://conwaylife.com/ref/lexicon/lex_s.htm) pattern:
```bash
sogol -w sawtooth --from-lexicon - << EOF
	.OO.OO
	..O.O.
	.O..O.
	.O.O..
	OO.OO.
EOF
```

## Motivation
This project was initially written for educational purposes in 2014. I was interested in simple sound synthesis project in python. Since then, it was left unmaintained for almost 7 years. Recently I was curios to play it again and I noticed few things:
* It was originally written for python2, which has reached EOL during that time.
* My programming skills and style changed a bit since then.
* It could have been written better.
* This is a great opportunity to integrate interesting utilities that I have not tinkered with before.

## Contributing
See [CONTRIBUTING.md](https://github.com/moyiz/sogol/blob/master/CONTRIBUTING.md)

## License
[BSD 3-Clause](https://github.com/moyiz/sogol/blob/master/LICENSE)

## Version
0.3.0
