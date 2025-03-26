import numpy as np

from utils.robot.robot import PrimitivesPolicy
from utils.io.io_utils import add_to_log

realrobot = True
policy = PrimitivesPolicy()


class Primitives:
    def __init__(self):
        pass

    def get_current_state(self):
        if realrobot:
            pose = policy.robot_env.robot.get_ee_pose()
            ee_pos = pose[0].numpy()
            ee_ori = pose[1].numpy()
            return (ee_pos, ee_ori)
        else:
            return (np.array((1., 0., 0.)), np.array((1., 0., 0., 0.)))

    def get_horizontal_ori(self):
        return policy.get_horizontal_ori()

    def get_vertical_ori(self):
        return policy.get_vertical_ori()

    def open_gripper(self, width=1):
        global gripper_opened
        if type(width) is not int and type(width) is not float:
            width = 1
        gripper_opened = True
        policy.open_gripper(width)

    def close_gripper(self, width=None):
        global gripper_opened
        if gripper_opened:
            check_grasp = True
        else:
            check_grasp = False
        if width is None:
            policy.close_gripper(check_grasp=check_grasp)
        else:
            if type(width) is not int and type(width) is not float:
                width = 1
            policy.open_gripper(width)

    def get_ori(self, degrees, axis):
        return policy.rotate_gripper(degrees, axis)

    def move_gripper_to_pose(self, pos, rot):
        return policy.move_to_pos(pos, rot)

    def parse_pos(self, pos_description, reference_frame='object'):
        global corr_rounds
        reference_frame = str(reference_frame)
        if reference_frame != "object" and reference_frame != "absolute":
            reference_frame = 'absolute'
        numpy_array = extract_array_from_str(pos_description)
        if numpy_array is None:
            ret_val, code_as_policies = _parse_pos(pos_description, reference_frame)
            if not any(char.isdigit() for char in pos_description):
                new_pos_description = replace_description_with_value(code_as_policies, pos_description)
                replace_code_with_no_description(new_pos_description, corr_rounds)
            return ret_val
        else:
            current_pos, _ = get_current_state()
            replace = False
            if np.linalg.norm(current_pos - numpy_array) < 0.008:
                pos_description = replace_strarray_with_str(pos_description, "current position")
                replace = True
            ret_val, code_as_policies = _parse_pos(pos_description, reference_frame)
            if replace:
                if not any(char.isdigit() for char in pos_description):
                    new_pos_description = replace_description_with_value(code_as_policies, pos_description)
                    replace_code_with_no_description(new_pos_description, corr_rounds)
            else:
                if not any(char.isdigit() for char in pos_description.split('[')[0]):
                    new_pos_description = replace_description_with_value(code_as_policies, pos_description)
                    replace_code_with_no_description(new_pos_description, corr_rounds)
            return ret_val

    def parse_ori(self, ori_description):
        ori_description = ori_description.split(' relative')[0]
        whole_prompt = prompt_parse_ori + '\n' + '\n' + f"# Query: {ori_description}" + "\n"
        response = query_LLM(whole_prompt, ["# Query:"], "cache/llm_response_parse_ori.pkl")
        code_as_policies = response.text
        add_to_log('-' * 80)
        add_to_log('*at parse_ori*')
        add_to_log(code_as_policies)
        add_to_log('-' * 80)
        localss = {}
        exec(code_as_policies, globals(), localss)
        return localss['ret_val']

    def reset_to_default_pose(self, ):
        return policy.reset()

    def get_task_pose(self, task):
        global rel_pos, rel_ori
        if rel_pos is None:
            pos, ori = _get_task_pose(task, visualize=True)
            return pos, ori
        else:
            pos, ori = _get_task_pose(task, visualize=False)
            assert len(ori) == 4
            real_pos, real_ori = get_real_pose(pos, ori, rel_pos, rel_ori)
            rel_pos, rel_ori = None, None
            return real_pos, real_ori

    def get_task_detection(self, task):
        return _get_task_detection(task)

    def change_reference_frame(self, wrong_direction, correct_direction):
        _change_reference_frame(wrong_direction, correct_direction)

    def execute_post_action(self, step_name):
        if "open" in step_name.lower() or "close" in step_name.lower():
            current_pos, current_ori = get_current_state()
            target_pos = parse_pos(f"a point 8cm back to {current_pos}.", reference_frame='object')
            move_gripper_to_pose(target_pos, current_ori)
            reset_to_default_pose()
        if "put" in step_name.lower():
            current_pos, current_ori = get_current_state()
            target_pos = parse_pos(f"a point 60cm above {current_pos}.", reference_frame='absolute')
            move_gripper_to_pose(target_pos, current_ori)
            reset_to_default_pose()
        if "pick" in step_name.lower():
            current_pos, current_ori = get_current_state()
            target_pos = parse_pos(f"a point 60cm above {current_pos}.", reference_frame='absolute')
            move_gripper_to_pose(target_pos, current_ori)
