import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
import launch

import xacro

def generate_launch_description():

    robotXacroName='vidhyut'

    namePackage = 'vidhyut'

    modelFile = 'model/vidhyut.xacro'

    worldFile = 'world/green_world.world'

    pathModelFile = os.path.join(get_package_share_directory(namePackage), modelFile)

    pathWorldFile = os.path.join(get_package_share_directory(namePackage), worldFile)

    robotDescription = xacro.process_file(pathModelFile).toxml()
    
    gazebo_rosPackageLaunch=PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py'))

    gazeboLaunch = IncludeLaunchDescription(gazebo_rosPackageLaunch, launch_arguments={'world': pathWorldFile}.items())

    spawnModelNode = Node(package='gazebo_ros', executable='spawn_entity.py', arguments=['-topic','robot_description','-entity',robotXacroName], output='screen')
    
    nodeRobotStatePublisher = Node(package='robot_state_publisher', executable='robot_state_publisher', output='screen', parameters=[{'robot_description': robotDescription},{'use_sim_time': True}])
    
    ld = LaunchDescription()

    ld.add_action(gazeboLaunch)
    ld.add_action(spawnModelNode)
    ld.add_action(nodeRobotStatePublisher)  
    

    return ld