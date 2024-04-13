import QtQuick

Rectangle {
    id: legend
    color: "white"

    property alias name: label.text
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
