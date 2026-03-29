from glob import glob

from setuptools import find_packages, setup

package_name = 'main_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.py')),
        ('share/' + package_name + '/description', glob('description/*')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools', 'pyserial'],
    zip_safe=True,
    maintainer='liam',
    maintainer_email='liamshan13@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'motor_serial_node = main_pkg.motor_serial_node:main',
            'odometry_node = main_pkg.odometry_node:main',
            'wheel_joint_state_node = main_pkg.wheel_joint_state_node:main',
        ],
    },
)
