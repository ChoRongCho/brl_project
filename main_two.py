import math
import time

import numpy as np
import pybullet as p
import pybullet_data
import random

def deg_to_rad(degrees):
    """도를 라디안(π 단위)으로 변환"""
    return degrees * (math.pi / 180)


def main():
    p.connect(p.GUI)  # or p.DIRECT for non-graphical version
    p.setAdditionalSearchPath(pybullet_data.getDataPath())  # used by loadURDF
    p.setGravity(0, 0, -10)

    urdf_path = "/home/changmin/PycharmProjects/brl/data/hand_urdf_description/urdf/bluehand.urdf"
    deg = np.array([80, 0, 0])
    handStartOrientation = p.getQuaternionFromEuler(list(deg_to_rad(deg)))
    handID = p.loadURDF(urdf_path, basePosition=[0, 0, 0.0], baseOrientation=handStartOrientation,
                        globalScaling=2.0, useFixedBase=True)

    planeId = p.loadURDF("plane.urdf", [0, 0, 0])

    num_of_joint = p.getNumJoints(handID)
    print("\n\n")
    print("[INFO] Num of Joint: ", num_of_joint)

    for i in range(num_of_joint):
        joint_info = p.getJointInfo(handID, i)
        # print(f"[INFO] {i} Joint: ", joint_info)

    movable_joints = []
    for j_index in range(num_of_joint):
        joint_info = p.getJointInfo(handID, j_index)
        joint_type = joint_info[2]  # Joint type (0: revolute, 1: prismatic, 2: spherical, 3: planar, 4: fixed)

        if joint_type in [p.JOINT_REVOLUTE]:  # 회전 가능 조인트만 선택
            movable_joints.append(j_index)

    count = 0
    while True:
        p.stepSimulation()
        time.sleep(1 / 240)

        if count > 100:
            random_pose = random.uniform(-5.0, 5.0)
            p.setJointMotorControl2(handID, 5, controlMode=p.POSITION_CONTROL, targetPosition=random_pose, force=5)

        # keys = p.getKeyboardEvents()
        # if len(keys) > 0:
        #     print("[INFO] Keyboard event: Quit the simulation")
        #     break

        count += 1

    p.disconnect()


if __name__ == '__main__':
    main()
