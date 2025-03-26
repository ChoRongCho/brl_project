import sys
import rclpy
from rclpy.node import Node
import Command  # 커스텀 메시지 Command.msg 불러오기
from PyQt5 import QtWidgets


class RobotControlApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """GUI 초기화"""

        self.setWindowTitle("Franka Panda Control")
        self.setGeometry(500, 800, 400, 300)

        # Object 입력 필드
        self.object_label = QtWidgets.QLabel("Object:", self)
        self.object_label.setGeometry(10, 10, 60, 30)
        self.object_input = QtWidgets.QLineEdit(self)
        self.object_input.setPlaceholderText("Enter object name")
        self.object_input.setGeometry(80, 10, 300, 30)
        self.object_input.returnPressed.connect(self.process_input)  # Enter 키 연결

        # Pose 입력 필드
        self.pose_label = QtWidgets.QLabel("Target Pose (x, y, z):", self)
        self.pose_label.setGeometry(10, 60, 150, 30)

        self.pose_x_input = QtWidgets.QLineEdit(self)
        self.pose_x_input.setPlaceholderText("x")
        self.pose_x_input.setGeometry(10, 100, 100, 30)
        self.pose_x_input.returnPressed.connect(self.process_input)  # Enter 키 연결

        self.pose_y_input = QtWidgets.QLineEdit(self)
        self.pose_y_input.setPlaceholderText("y")
        self.pose_y_input.setGeometry(120, 100, 100, 30)
        self.pose_y_input.returnPressed.connect(self.process_input)  # Enter 키 연결

        self.pose_z_input = QtWidgets.QLineEdit(self)
        self.pose_z_input.setPlaceholderText("z")
        self.pose_z_input.setGeometry(230, 100, 100, 30)
        self.pose_z_input.returnPressed.connect(self.process_input)  # Enter 키 연결

        # Submit 버튼
        self.submit_button = QtWidgets.QPushButton("Submit", self)
        self.submit_button.setGeometry(150, 150, 100, 30)
        self.submit_button.clicked.connect(self.process_input)

        # 상태 레이블
        self.status_label = QtWidgets.QLabel(self)
        self.status_label.setGeometry(10, 200, 380, 30)

    def process_input(self):
        """입력된 명령을 처리하는 메서드"""
        object_command = self.object_input.text()
        pose_x = self.pose_x_input.text()
        pose_y = self.pose_y_input.text()
        pose_z = self.pose_z_input.text()

        # 입력 필드 비우기
        self.object_input.clear()
        self.pose_x_input.clear()
        self.pose_y_input.clear()
        self.pose_z_input.clear()

        # 메시지 생성 및 퍼블리시
        msg = Command()
        msg.object_name = object_command
        msg.x = pose_x
        msg.y = pose_y
        msg.z = pose_z
        self.publisher.publish(msg)

        self.status_label.setText(f"Published: {object_command} -> [{pose_x}, {pose_y}, {pose_z}]")



def main(args=None):
    rclpy.init(args=args)
    node = Node('robot_control_publisher')
    publisher = node.create_publisher(Command, 'robot_commands', 10)

    app = QtWidgets.QApplication(sys.argv)
    ex = RobotControlApp(publisher)
    ex.show()

    rclpy.spin(node)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
