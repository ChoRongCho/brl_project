from setuptools import find_packages, setup

package_name = 'basic_commu'

# setup(
#     name=package_name,
#     version='0.0.0',
#     packages=find_packages(exclude=['test']),
#     data_files=[
#         ('share/ament_index/resource_index/packages',
#             ['resource/' + package_name]),
#         ('share/' + package_name, ['package.xml']),
#     ],
#     install_requires=['setuptools'],
#     zip_safe=True,
#     maintainer='changmin',
#     maintainer_email='cmp9877@gmail.com',
#     description='TODO: Package description',
#     license='TODO: License declaration',
#     tests_require=['pytest'],
#     entry_points={
#         'console_scripts': [
#         ],
#     },
# )

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    py_modules=['publisher', 'subscriber'],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='changmin',
    maintainer_email='cmp9877@naver.com',
    description='A simple ROS 2 package for publisher and subscriber.',
    license='License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publisher = my_ros2_package.publisher:main',
            'subscriber = my_ros2_package.subscriber:main',
        ],
    },
)
