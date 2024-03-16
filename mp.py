#!/usr/bin/manage_photos/venv/bin/python

import shutil
from pathlib import Path

import typer
from send2trash import send2trash

app = typer.Typer()


def _move_photos(path: Path):
    if not path.is_dir():
        return

    raw_photos = [f for f in path.iterdir() if f.suffix.lower() in {'.raw', '.raf'}]

    # move raw photos to a folder
    raw_dir = (path / 'raw')
    raw_dir.mkdir(exist_ok=True)
    for f in raw_photos:
        shutil.move(f, raw_dir)

    print(f'Moved {len(raw_photos)} photos')


@app.command()
def move(path: str, r: bool = False):
    """
    Move all raw photos to the `raw` subdirectory
    :param path: Where are the photos
    :param r: Process all directories in the current directory
    :return:
    """
    data_path = Path(path)

    if r:
        for photo_dir in data_path.iterdir():
            _move_photos(photo_dir)
    else:
        _move_photos(data_path)


@app.command()
def cleanup(path: str):
    """
    Delete raw photos in the `raw` subdirectory if they don't have a pair in jpeg photos in the main dir
    :param path: Where are the photos
    :return:
    """

    cleanup_raws(Path(path))


def cleanup_raws(path: Path):
    jpeg_photos = [f for f in path.iterdir() if f.suffix.lower() in {'.jpg', '.jpeg'}]

    raw_dir = (path / 'raw')
    if not raw_dir.exists():
        raise Exception('No raw dir')

    raw_photos = [f for f in raw_dir.iterdir() if f.suffix.lower() in {'.raw', '.raf'}]
    if not raw_photos:
        raise Exception('No raw photos in raw dir')

    jpeg_stems = set([f.stem for f in jpeg_photos])
    raw_stems = set([f.stem for f in raw_photos])

    files_to_del = raw_stems - jpeg_stems
    files_to_del = {f for f in raw_photos if f.stem in files_to_del}

    for f in files_to_del:
        print(f'Deleting {str(f)}')
        send2trash(f)


if __name__ == '__main__':
    app()
