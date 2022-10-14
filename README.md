# xfz-accounting

## develop

* install toolkit
  * install Qt6 from https://www.qt.io/
  * install PyQt6 using `pip3 install PyQt6`
* generate translation
  * generate blank translation file using `~/Qt/6.4.0/macos/bin/lupdate accounting.pro`
  * use `~/Qt/6.4.0/macos/bin/Linguist.app` to edit translation file
  * use `~/Qt/6.4.0/macos/bin/lrelease` to generate compiled translation file
* generate resources
  * `~/Qt/6.4.0/macos/libexec/rcc --g python -o resources.py resources.qrc`
  * edit `resources.py`, change `from PySide6 import QtCore` to `from PyQt6 import QtCore`
* enjoy the app

