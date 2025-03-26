import numpy as np


def main():

    while True:

        li = input('\n\n\n' + "I'm ready to take instruction." + '\n' + 'Input your instruction:')

        """
        1. initialize detection
        2. get object initial state
        3. get object list or dict
        4. print
        """

        """
        1. li 로부터 관련된 정보를 검색
        2. prompt_plan_instance.set_object_state(obj_state)
        3. prompt_plan_instance.add_constraints(plan_related_info)
        object state와 관련된 정보를 prompt에 추가
        """

        """
        # Generate initial plans (which could only be wrong in not grounding objects)
        prompt_plan = prompt_plan_instance.get_prompt()
        whole_prompt = prompt_plan + '\n' + '\n' + f"Instruction: {li}" + "\n"
        response = query_LLM(whole_prompt, ["Instruction:"], "cache/llm_response_planning_high.pkl")
        raw_code_step = format_plan(response)
        print('***raw plan***')
        print(raw_code_step)
        """
