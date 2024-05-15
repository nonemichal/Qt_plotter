import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts
import QtCharts

// Main window
ApplicationWindow {
    id: root
    width: 640
    height: 480
    color: "white"
    visible: true
    title: qsTr("Plotter")

    property string dataName

    // Menu bar on the top of program
    menuBar: MenuBar {
        Menu {
            title: qsTr("&File")
            MenuItem {
                text: qsTr("&Open...")
                icon.name: "document-open"
                onTriggered: {
                    customChart.holdOn = false;
                    fileOpenDialog.open();
                }
            }
            MenuItem {
                text: qsTr("&Save")
                icon.name: "document-save"
                onTriggered: saveChart(dataName + ".png")
            }
            MenuItem {
                text: qsTr("Save &As...")
                icon.name: "document-save-as"

            }
            MenuItem {
                text: qsTr("Add series")
                onTriggered: {
                    customChart.holdOn = true;
                    fileOpenDialog.open();
                }
            }
        }

        Menu {
            title: qsTr("&Help")
            MenuItem {
                text: qsTr("&About...")
                onTriggered: aboutDialog.open()
            }
        }
    }

    // File dialog to open .csv files
    FileDialog {
        id: fileOpenDialog
        title: "File dialog"
        currentFolder: StandardPaths.standardLocations(StandardPaths.HomeLocation)[0]
        nameFilters: ["CSV files (*.csv)"]
        onAccepted: {
            var path = selectedFile.toString();
            path = path.replace(/^(file:\/{3})|(qrc:\/{2})|(http:\/{2})/,"/");;
            customChart.newData(path);
        }
    }

    // Dialog which provides informations about program
    Dialog {
        id: aboutDialog
        width: 300
        height: 200
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        modal: false
        standardButtons: Dialog.Ok
        title: qsTr("About")

        header: ToolBar {
            background: Rectangle {
                color: "#303030"
            }
            RowLayout {
                anchors.fill: parent
                Label {
                    text: "About"
                    elide: Label.ElideRight
                    horizontalAlignment: Qt.AlignHCenter
                    verticalAlignment: Qt.AlignVCenter
                    Layout.fillWidth: true
                }
                ToolButton {
                    text: qsTr("x")
                    onClicked: aboutDialog.close()
                }
            }
        }

        Label {
            text: "Lorem ipsum..."
            anchors.fill: parent
        }
    }

    // Main window is made of 2 columns
    Column {
        id: column
        anchors.fill: parent
        spacing: 0

        // Chart column
        CustomChart {
            id: customChart
            width: parent.width
            height: parent.height - customLegend.height
            onUpdated: (seriesName, seriesColor) => {
                dataName = seriesName;
                customLegend.name = seriesName;
                customLegend.color = seriesColor;
            }
        }

        // Legend column
        CustomLegend {
            id: customLegend
            width: parent.width
            height: 50
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }

    // Function to save chart as an image
    function saveChart(filename){
        customChart.grabToImage(function(result) {
            result.saveToFile(filename);
        });
    }
}
