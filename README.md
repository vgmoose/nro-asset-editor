## nro-asset-editor
Edit asset data in Switch homebrew .nro files according to the Assets layout described on [switchbrew](http://switchbrew.org/index.php?title=NRO#Assets).

Using this program it should be possible to add/change icons and metadata for any hbmenu homebrew apps. It can be downloaded from the [release page](https://github.com/vgmoose/nro-asset-editor/releases).

### GUI
To run the GUI, either run the precompiled binary from the release page, or run `maker.py` without any additional arguments.

### Command Line
```
python3 maker.py [--nro /path/to/file.nro] [--title \"Your App Title\"] [--icon /path/to/icon.(png|jpg)] [--author \"Your Author\"] [--version x.x.x]")
```

When running, it will output the before and after NRO information. Any arguments omitted will retain their value from before running the script.
