# Simon Stålenhag Wallpaper Downloader

Downloads all wallpapers from [simonstalenhag.se](https://www.simonstalenhag.se) to `~/Pictures/Stålenhag/`.

## Usage

```sh
# Download all wallpapers
python stalenhag.py --all

# List available wallpapers
python stalenhag.py --list

# Help
python stalenhag.py --help
```

Or with [uv](https://docs.astral.sh/uv/):

```sh
uv run stalenhag --all
uv run stalenhag --list
```

## Install

```sh
uv sync
uv run stalenhag --all
```

## Output

All wallpapers are saved to `~/Pictures/Stålenhag/`.
