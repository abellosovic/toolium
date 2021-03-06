# -*- coding: utf-8 -*-
u"""
Copyright 2015 Telefónica Investigación y Desarrollo, S.A.U.
This file is part of Toolium.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os

import pytest

from toolium.config_files import ConfigFiles
from toolium.driver_wrapper import DriverWrapper
from toolium.driver_wrappers_pool import DriverWrappersPool


@pytest.fixture
def driver_wrapper():
    # Reset wrappers pool values
    DriverWrappersPool._empty_pool()

    # Create default wrapper
    driver_wrapper = DriverWrappersPool.get_default_wrapper()

    # Configure properties
    config_files = ConfigFiles()
    root_path = os.path.dirname(os.path.realpath(__file__))
    config_files.set_config_directory(os.path.join(root_path, 'conf'))
    config_files.set_output_directory(os.path.join(root_path, 'output'))
    driver_wrapper.configure(tc_config_files=config_files)

    return driver_wrapper


def test_singleton(driver_wrapper):
    # Request default wrapper
    new_wrapper = DriverWrappersPool.get_default_wrapper()

    # Modify new wrapper
    new_driver_type = 'opera'
    new_wrapper.config.set('Driver', 'type', new_driver_type)

    # Check that both wrappers are the same object
    assert new_driver_type == driver_wrapper.config.get('Driver', 'type')
    assert new_driver_type == new_wrapper.config.get('Driver', 'type')
    assert driver_wrapper == new_wrapper
    assert DriverWrappersPool.driver_wrappers[0] == driver_wrapper


def test_multiple(driver_wrapper):
    # Request a new additional wrapper
    new_wrapper = DriverWrapper()

    # Check that wrapper and new_wrapper are different
    assert driver_wrapper != new_wrapper
    assert DriverWrappersPool.driver_wrappers[0] == driver_wrapper
    assert DriverWrappersPool.driver_wrappers[1] == new_wrapper


def test_find_parent_directory_relative():
    directory = 'conf'
    filename = 'properties.cfg'
    expected_config_directory = os.path.join(os.getcwd(), 'conf')

    assert expected_config_directory == DriverWrappersPool._find_parent_directory(directory, filename)


def test_find_parent_directory_file_not_found():
    directory = 'conf'
    filename = 'unknown'
    expected_config_directory = os.path.join(os.getcwd(), 'conf')

    assert expected_config_directory == DriverWrappersPool._find_parent_directory(directory, filename)


def test_find_parent_directory_absolute():
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'conf')
    filename = 'properties.cfg'
    expected_config_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'conf')

    assert expected_config_directory == DriverWrappersPool._find_parent_directory(directory, filename)


def test_find_parent_directory_absolute_recursively():
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'unknown', 'conf')
    filename = 'properties.cfg'
    expected_config_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'conf')

    assert expected_config_directory == DriverWrappersPool._find_parent_directory(directory, filename)
