# SPDX-FileCopyrightText: NVIDIA CORPORATION & AFFILIATES
# Copyright (c) 2023 TINKER TWINS. All rights reserved.
# Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
from isaac_ros_launch_utils.all_types import *
import isaac_ros_launch_utils as lu

from nvblox_ros_python_utils.nvblox_launch_utils import NvbloxMode, NvbloxCamera
from nvblox_ros_python_utils.nvblox_constants import NVBLOX_CONTAINER_NAME


def generate_launch_description() -> LaunchDescription:
    args = lu.ArgumentContainer()
    args.add_arg('log_level', 'info')
    args.add_arg('num_cameras', 1)
    args.add_arg('mode', default=NvbloxMode.static, cli=True)
    args.add_arg('run_rviz', default='True')
    args.add_arg('use_foxglove_whitelist', True)
    args.add_arg('container_name', NVBLOX_CONTAINER_NAME)
    args.add_arg('global_frame', default='odom')

    actions = args.get_launch_actions()

    actions.append(
        Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='camera_mount_tf',
        arguments=['0.015', '0', '0.122', '0', '0', '0', '1', 'base_link', 'camera0_link'],
        )
        
    )

    # Start container early so composables can be loaded
    actions.append(
        lu.component_container(args.container_name, log_level=args.log_level)
    )

    # Launch Realsense camera
    actions.append(
        lu.include(
            'nvblox_examples_bringup',
            'launch/sensors/realsense.launch.py',
            launch_arguments={
                'container_name': args.container_name,
                'num_cameras': args.num_cameras
            }
        )
    )

    # Launch Visual SLAM
    actions.append(
        lu.include(
            'nvblox_examples_bringup',
            'launch/perception/vslam.launch.py',
            launch_arguments={
                'container_name': args.container_name,
                'camera': str(NvbloxCamera.realsense),
                'output_odom_frame_name': args.global_frame
            }
        )
    )

    # Launch NVBlox Mapping
    actions.append(
        lu.include(
            'nvblox_examples_bringup',
            'launch/perception/nvblox.launch.py',
            launch_arguments={
                'container_name': args.container_name,
                'mode': args.mode,
                'camera': str(NvbloxCamera.realsense),
                'num_cameras': args.num_cameras
            }
        )
    )

    # Launch Nav2
    actions.append(
        lu.include(
            'nvblox_examples_bringup',
            'launch/nav2/nav2_realsense.launch.py'
        )
    )

    # Optional: RViz
    actions.append(
        lu.include(
            'nvblox_examples_bringup',
            'launch/visualization/visualization.launch.py',
            launch_arguments={
                'mode': args.mode,
                'camera': str(NvbloxCamera.realsense),
                'use_foxglove_whitelist': args.use_foxglove_whitelist
            },
            condition=IfCondition(args.run_rviz)
        )
    )

    return LaunchDescription(actions)