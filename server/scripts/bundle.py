# NOTE: This should be run in the server directory.
import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "app.py",
        "--onefile",
        "--name=NetSpiderServer",
        "--hidden-import=gevent",
        "--hidden-import=engineio.async_drivers.gevent",
        "--hidden-import=pyimod02_importers",
        "--add-data=Backend/schema/:Backend/schema/",
    ]
)
