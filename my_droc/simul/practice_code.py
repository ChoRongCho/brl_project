import time

import numpy as np
import pybullet as p
import pybullet_data


class DiveInPybullet:
    def __init__(self):
        self.gravity = -9.8

        self.robot_name = "franka_panda/panda.urdf"
        self.table_name = "table/table.urdf"
        self.cup_name = "urdf/mug.urdf"
        self.jenga_name = "jenga/jenga.urdf"
        self.cube_name = "cube_small.urdf"

        self.object_list = [self.cup_name, self.jenga_name, self.cube_name]

        p.connect(p.GUI)
        print(pybullet_data.getDataPath())
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, self.gravity)

        self.load_env()

    def load_env(self):
        angle = np.radians(90)  # 90도를 라디안으로 변환
        qx = 0
        qy = 0
        qz = np.sin(angle / 2)  # 회전축 Z축
        qw = np.cos(angle / 2)
        table_orientation = [qx, qy, qz, qw]  # 쿼터니언 형태로 설정

        rand = np.random.uniform(0.7, 1.3, 6)

        p.loadURDF("plane.urdf", basePosition=[0, 0, 0])  # 바닥 추가
        p.loadURDF(self.robot_name, basePosition=[0, 0, 0], useFixedBase=True)
        p.loadURDF(self.table_name, basePosition=[1, 0, 0], baseOrientation=table_orientation)  # 테이블 추가
        p.loadURDF(self.cup_name, basePosition=[rand[0], rand[1]-1, 1])  # 컵 추가
        p.loadURDF(self.jenga_name, basePosition=[rand[2], rand[3]-1, 1], baseOrientation=table_orientation)  # 젠가 추가
        p.loadURDF(self.cube_name, basePosition=[rand[4], rand[5]-1, 1])  # cube 추가

    def reset(self):
        p.resetSimulation()
        p.setGravity(0, 0, self.gravity)
        self.load_env()

    def run(self):
        while True:
            keys = p.getKeyboardEvents()
            if ord('r') in keys and keys[ord('r')] & p.KEY_WAS_TRIGGERED:  # 'R' 키가 눌리면
                self.reset()
            elif ord('q') in keys and keys[ord('q')] & p.KEY_WAS_TRIGGERED:  # 'R' 키가 눌리면
                break
            p.stepSimulation()
            time.sleep(1. / 240.)

    # robot
    def move_to_object(self, object_position):
        """객체의 위치로 이동하여 잡는 메서드"""
        joint_angles = p.calculateInverseKinematics(
            self.robot_id,
            endEffectorLinkIndex=7,  # 엔드 이펙터 링크 인덱스
            targetPosition=object_position,
            targetOrientation=p.getQuaternionFromEuler([0, 0, 0])  # 자유 회전
        )
        self.apply_joint_angles(joint_angles)

    def place_object(self, target_pose):
        """지정된 위치로 객체를 옮기는 메서드"""
        joint_angles = p.calculateInverseKinematics(
            self.robot_id,
            endEffectorLinkIndex=7,
            targetPosition=target_pose,
            targetOrientation=p.getQuaternionFromEuler([0, 0, 0])
        )
        self.apply_joint_angles(joint_angles)

    def apply_joint_angles(self, joint_angles):
        """조인트 각도를 로봇에 적용하는 메서드"""
        for i in range(len(joint_angles)):
            p.setJointMotorControl2(self.robot_id, i, p.POSITION_CONTROL, joint_angles[i])
        p.stepSimulation()

    def is_within_workspace(self, target_position):
        """타겟 위치가 로봇의 가동 범위 내에 있는지 확인하는 메서드"""
        # 이 부분은 실제 로봇의 작업 공간에 따라 조정해야 합니다.
        # 여기서는 단순한 범위 체크 예시를 제공합니다.
        x, y, z = target_position
        return all([-1 <= x <= 1, -1 <= y <= 1, 0 <= z <= 1])


def main():
    sim = DiveInPybullet()
    sim.run()


if __name__ == '__main__':
    main()
