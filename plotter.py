import polars as pl
import time

from PySide6.QtCore import  QObject, Slot, QPointF
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis

class Plotter(QObject):
    # Limit values
    minX = 0
    maxX = 0
    minY = 0
    maxY = 0
    values = dict.fromkeys(["time", "abp", "icp", "fvl", "fvr"])
    valuesLen = 0

    # Names of .csv files
    fileNames = []

    # Fills plot with provided fillSeries
    @Slot(str)
    def initialize(self, path):
        self.fileNames.append(path)
        df = pl.read_csv(path)

        self.values["time"] = [t - df.get_column("DateTime")[0] for t in df.get_column("DateTime")]
        self.values["abp"] = df.get_column("abp[mmHg]")
        self.values["icp"] = df.get_column("icp[mmHg]")
        self.values["fvl"] = df.get_column("fvl[cm/s]")
        self.values["fvr"] = df.get_column("fvr[cm/s]")
        self.valuesLen = len(self.values["time"])

        self.vals_range = [self.valuesLen-60, self.valuesLen]

    @Slot(QLineSeries, QLineSeries, QLineSeries, QLineSeries)
    def fillSeries(self, abp, icp, fvl, fvr):
        #for i in range(self.valuesLen):
        #    abp.append(self.values["time"][i], self.values["abp"][i])
        #    icp.append(self.values["time"][i], self.values["icp"][i])
        #    fvl.append(self.values["time"][i], self.values["fvl"][i])
        #    fvr.append(self.values["time"][i], self.values["fvr"][i])
        #
        #    print(self.values["time"][i])

        start_time = time.time()

        abp_points = [QPointF(x, y) for x, y in zip(self.values["time"][self.vals_range[0]:self.vals_range[1]], self.values["abp"][self.vals_range[0]:self.vals_range[1]])]
        icp_points = [QPointF(x, y) for x, y in zip(self.values["time"][self.vals_range[0]:self.vals_range[1]], self.values["icp"][self.vals_range[0]:self.vals_range[1]])]
        fvl_points = [QPointF(x, y) for x, y in zip(self.values["time"][self.vals_range[0]:self.vals_range[1]], self.values["fvl"][self.vals_range[0]:self.vals_range[1]])]
        fvr_points = [QPointF(x, y) for x, y in zip(self.values["time"][self.vals_range[0]:self.vals_range[1]], self.values["fvr"][self.vals_range[0]:self.vals_range[1]])]

        abp.append(abp_points)
        icp.append(icp_points)
        fvl.append(fvl_points)
        fvr.append(fvr_points)

        print("--- %s seconds ---" % (time.time() - start_time))



    # Sets axes limits
    # Objects contains current limits and compares it with new ones
    @Slot(QValueAxis, QValueAxis)
    def setAxes(self, xAxis, yAxis):
        minX = min(self.values["time"][self.vals_range[0]:self.vals_range[1]])
        maxX = max(self.values["time"][self.vals_range[0]:self.vals_range[1]])
        minY = min(self.values["abp"][self.vals_range[0]:self.vals_range[1]])
        maxY = max(self.values["abp"][self.vals_range[0]:self.vals_range[1]])

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
        yAxis.setProperty('min', minY)
        yAxis.setProperty('max', maxY)

    # Clears current Plotter object
    @Slot()
    def clearObject(self):
        # Limit values
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0
        self.values = dict.fromkeys(["time", "abp", "icp", "fvl", "fvr"])
        self.valuesLen = 0

        # Names of .csv files
        self.fileNames = []

    # Checks if the file was already provided
    @Slot(str, result=bool)
    def isFile(self, path):
        return path in self.fileNames
