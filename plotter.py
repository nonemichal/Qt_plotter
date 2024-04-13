import polars as pl

from PySide6.QtCore import  QObject, Slot, QPointF
from PySide6.QtCharts import QScatterSeries, QLineSeries, QValueAxis

class Plotter(QObject):
    minX = 0
    maxX = 0
    minY = 0
    maxY = 0
    fileNames = []

    @Slot(QScatterSeries, QLineSeries, str)
    def fillSeries(self, scatter, line, path):
        self.fileNames.append(path)
        df = pl.read_csv(path)
        self.columnNames = df.columns
        self.xValues = df[self.columnNames[0]]
        self.yValues = df[self.columnNames[1]]

        line.setProperty("color", scatter.color())

        for i in range(0, len(self.xValues)):
            point = QPointF(self.xValues[i], self.yValues[i])
            scatter.append(point)
            line.append(point)

    @Slot(QValueAxis, QValueAxis)
    def setAxes(self, xAxis, yAxis):
        minX = min(self.xValues)
        maxX = max(self.xValues)
        minY = min(self.yValues)
        maxY = max(self.yValues)

        self.minX = minX if minX < self.minX else self.minX
        self.maxX = maxX if maxX > self.maxX else self.maxX
        self.minY = minY if minY < self.minY else self.minY
        self.maxY = maxY if maxY > self.maxY else self.maxY

        minX  = self.minX - abs(self.maxX - self.minX) * 0.2
        maxX  = self.maxX + abs(self.maxX - self.minX) * 0.2
        minY  = self.minY - abs(self.maxY - self.minY) * 0.2
        maxY  = self.maxY + abs(self.maxY - self.minY) * 0.2

        xAxis.setProperty('min', minX)
        xAxis.setProperty('max', maxX)
        xAxis.setProperty('titleText', self.columnNames[0])
        yAxis.setProperty('min', minY)
        yAxis.setProperty('max', maxY)
        yAxis.setProperty('titleText', self.columnNames[1])

    @Slot()
    def clearObject(self):
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0
        self.fileNames = []
        self.columnNames = []
        self.xValues = []
        self.yValues = []

    @Slot(str, result=bool)
    def isFile(self, path):
        return path in self.fileNames
