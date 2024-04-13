import QtQuick
import QtQuick.Controls
import QtCharts
import Plotters

ChartView {
    id: root
    antialiasing: true
    legend.visible: false
    title: " "

    signal updated(seriesName: string, seriesColor: color)
    signal newData(fileUrl: string)
    property bool holdOn

    Plotter {
        id: plotter
    }

    ValueAxis {
            id: myAxisX
            titleText: "x"
        }

    ValueAxis {
            id: myAxisY
            titleText: "y"
        }

    Component.onCompleted: {
        var scatter = root.createSeries(ChartView.SeriesTypeScatter, "scatter", myAxisX, myAxisY);
    }

    Connections {
        target: root
        function onNewData(fileUrl) {
            if (!holdOn) {
                root.removeAllSeries();
                plotter.clearObject();
            }

            if (!plotter.isFile(fileUrl)) {
                var scatter = root.createSeries(ChartView.SeriesTypeScatter, "scatter", myAxisX, myAxisY);
                var line = root.createSeries(ChartView.SeriesTypeLine, "line", myAxisX, myAxisY);

                plotter.fillSeries(scatter, line, fileUrl);
                plotter.setAxes(myAxisX, myAxisY);

                var name = fileUrl.substring(0, fileUrl.length - 4).replace(/^.*[\\/]/, '');
                var color = scatter.color;
                root.title = name;
                root.updated(name, color);
            }
        }
    }

    Rectangle {
        id: scrollMask
        visible: false
    }

    MouseArea {
        id: chartMouseArea
        anchors.fill: parent
        hoverEnabled: true
        acceptedButtons: Qt.LeftButton
        onDoubleClicked: plotter.setAxes(myAxisX, myAxisY);

        onMouseXChanged: (mouse) => {
            if ((mouse.buttons & Qt.LeftButton) == Qt.LeftButton) {
                root.scrollLeft(mouseX - scrollMask.x);
                scrollMask.x = mouseX;
            }
        }

        onMouseYChanged: (mouse) => {
            if ((mouse.buttons & Qt.LeftButton) == Qt.LeftButton) {
                root.scrollUp(mouseY - scrollMask.y);
                scrollMask.y = mouseY;
            }
        }

        onPressed: (mouse) => {
            if (mouse.button === Qt.LeftButton) {
                scrollMask.x = mouseX;
                scrollMask.y = mouseY;
            }
        }

        onWheel: (wheel)=> {
             if (wheel.angleDelta.y > 0) {
                 root.zoomIn();
             } else {
                 root.zoomOut();
             }
        }
    }
}
