

class Perception:
    def __init__(self):
        pass

    def detect(self, obj_name, visualize=False):
        pass

    def detect_objects(self,
                       load_from_cache=False,
                       run_on_server=False,
                       save_to_cache=True,
                       visualize=False):
        pass

    def segment_image(self, image):
        pass

    def save_current_image(self, image):
        pass

    def test_image(self, text):
        pass



# if __name__ == '__main__':
#     main()


