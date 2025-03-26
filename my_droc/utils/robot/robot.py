import numpy as np
from scipy.spatial.transform import Rotation

from utils.robot.env import Env

"""Hyperparameters"""
GRIPPER_SPEED, GRIPPER_FORCE, GRIPPER_MAX_WIDTH, GRIPPER_TOLERANCE = 0.1, 40, 0.08570, 0.01


def calculate_from_quat(g_x, g_z):
    base_x = np.array([1., 0., 0.])  # Replace with the X-axis vector of the base frame
    base_z = np.array([0., 0., 1.])  # Replace with the Z-axis vector of the base frame

    # Step 1: Calculate Y-axis vector of frame G in the base frame
    base_y = np.cross(base_z, base_x)
    base_y /= np.linalg.norm(base_y)

    # Step 2: Create rotation matrices for the base and frame G
    R_base = np.column_stack((base_x, base_y, base_z))
    R_g = np.column_stack((g_x, np.cross(g_z, g_x), g_z))

    # Step 3: Compute rotation matrix to transform frame G's axes to the base frame axes
    R_relative_to_base = np.dot(R_base.T, R_g)

    # Step 4: Convert the rotation matrix to a quaternion using scipy's Rotation class
    r = Rotation.from_matrix(R_relative_to_base)
    frame_quaternion = r.as_quat()
    return frame_quaternion


class PrimitivesPolicy:
    def __init__(self):
        self.robot_env = Env()
        self.robot_env.reset()

    def reset(self, reset_gripper=True):
        self.robot_env.reset(reset_gripper=reset_gripper)

    def close_gripper(self):
        pass

    def open_gripper(self):
        pass

    def rotate_gripper(self, degrees, axis):
        pass

    def move_to_pos(self, ee_pos, tar_quat):
        pass

    def rotate_around_gripper_z_axis(self, angle, quat=None):
        pass

    def tilt_left_right(self, degrees):
        pass

    def tilt_updown(self, degrees=None):
        pass

    def align_z_axis_with_vector(self, z_axis, finger_plane='vertical'):
        pass

    def robot_fingertip_pos_to_ee(self, fingertip_pos, ee_quat):
        pass

    def ee_pos_to_fingertip(self, ee_pos, ee_quat):
        pass

    def get_horizontal_ori(self):
        pass

    def get_vertical_ori(self):
        pass


def main():
    x = np.array([1, 1, 3])
    z = np.array([1, 2, 0])

    frame_qaut = calculate_from_quat(x, z)
    print(frame_qaut)


if __name__ == '__main__':
    main()
