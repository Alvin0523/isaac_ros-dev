#!/bin/bash
#####################################################################################
# SPDX-FileCopyrightText: Copyright (c) 2019 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
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
#####################################################################################

set -e  # Exit on error

# Source ROS root environment
source "${ROS_ROOT:?}/setup.bash"

# If a workspace is defined, build it if needed and source it
if [[ ! -z "${ROS_WS}" ]]; then
  # Build the workspace if src/ exists and install/ does not
  if [[ -d "${ROS_WS}/src" && ! -d "${ROS_WS}/install" ]]; then
    echo "Building ROS workspace at ${ROS_WS}..."
    cd "${ROS_WS}"
    colcon build --symlink-install
  fi

  # Source the workspace overlay if it exists
  if [[ -f "${ROS_WS}/install/setup.bash" ]]; then
    source "${ROS_WS}/install/setup.bash"
  fi
fi

set -x
exec "$@"