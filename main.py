# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType

import plotter

CURRENT_DIRECTORY = Path(__file__).resolve().parent

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    qmlRegisterType(plotter.Plotter, 'Plotters', 1, 0, 'Plotter')

    qml_file = CURRENT_DIRECTORY / "main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
