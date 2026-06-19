from setuptools import find_packages, setup

package_name = 'pose_reactive_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'pose_detector_node = pose_reactive_robot.pose_detector_node:main',
            'pet_state_classifier_node = pose_reactive_robot.pet_state_classifier_node:main',
            'robot_controller_node = pose_reactive_robot.robot_controller_node:main',
            'video_publisher_node = pose_reactive_robot.video_publisher_node:main',
        ],
    },
)
