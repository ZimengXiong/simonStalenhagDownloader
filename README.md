# Simon Stålenhag Wallpaper Downloader

Downloads all wallpapers from [simonstalenhag.se](https://www.simonstalenhag.se) to `~/Pictures/Stålenhag/`.

## Usage

With [uv](https://docs.astral.sh/uv/):

```sh
uv run stalenhag --all
uv run stalenhag --list
uv run stalenhag --help
```

## Install

```sh
uv sync
uv run stalenhag --all
```

Or run directly without installing:

```sh
uvx stalenhag --all
```

## Output

All wallpapers are saved to `~/Pictures/Stålenhag/`.
