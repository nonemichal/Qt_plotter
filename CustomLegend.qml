import QtQuick

// Legen as Rectangle object
Rectangle {
    id: legend
    color: "white"

    // Series name
    property alias name: label.text

    // Series color
    property alias color: marker.color

    Row {
        id: row
        spacing: 5
        anchors {
            horizontalCenter: parent.horizontalCenter
            verticalCenter: parent.verticalCenter
        }

        Rectangle {
            id: marker
            anchors.verticalCenter: parent.verticalCenter
            radius: 4
            width: 12
            height: 10
        }

        Text {
            id: label
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: -1
        }
    }
}
