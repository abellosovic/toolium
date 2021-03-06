.. _bdd_integration:

BDD Integration
===============

Toolium can be also used with behave and lettuce tests.

Behave
~~~~~~

Behave tests should be developed as usual, only *environment.py* file should be modified to initialize driver and the
rest of Toolium configuration.

Environment methods should call to the corresponding Toolium environment methods, as can be seen in the following
example:

.. code-block:: python

    from toolium.behave.environment import (before_all as toolium_before_all, before_scenario as toolium_before_scenario,
                                            after_scenario as toolium_after_scenario, after_all as toolium_after_all)


    def before_all(context):
        toolium_before_all(context)


    def before_scenario(context, scenario):
        toolium_before_scenario(context, scenario)


    def after_scenario(context, scenario):
        toolium_after_scenario(context, scenario)


    def after_all(context):
        toolium_after_all(context)


After initialization, the following attributes will be available in behave context:

- context.toolium_config: dictionary with Toolium configuration, readed from properties.cfg
- context.driver_wrapper: :ref:`DriverWrapper <driver_wrapper>` instance
- context.driver: Selenium or Appium driver instance
- context.utils: :ref:`Utils <utils>` instance

Behave userdata properties
--------------------------

Toolium properties can be modified from behave userdata configuration. For example, to select the driver type from
command line instead of using the driver type defined in properties.cfg:

.. code:: console

    $ behave -D Driver_type=chrome

Behave tags
-----------

Toolium defines two tags to configure driver:

* @reuse_driver: feature tag to indicate that all scenarios in this feature should share the driver. The browser will
not be closed between tests.
* @reset_driver: identifies a scenario that should not reuse the driver. The browser will be closed before this test.

And other scenario tags to configure Appium tests:

* @no_reset_app: mobile app will not be reset before test (i.e. no-reset Appium capability is set to true)
* @reset_app: mobile app will be reset before test (i.e. no-reset and full-reset Appium capabilities are set to false)
* @full_reset_app: mobile app will be full reset before test (i.e. full-reset Appium capability is set to true)
* @android_only: identifies a scenario that should only be executed in Android
* @ios_only: identifies a scenario that should only be executed in iOS

Behave - Dynamic Environment
----------------------------

Optionally, some actions (labels) are defined in the Feature description as:

* Actions Before the Feature:
* Actions Before each scenario:
* Actions after each scenario:
* Actions after the Feature:

With a steps list executed in each moment identified with the label as the environment.py file. These steps are defined
similar to others one.

Each step block is separated by a blank line.

Behave keywords are supported  (Given, When, Then, And, But, Check, Setup).

Example::

        Feature: Tests with the dynamic environment
          As a behave operator using multiples scenarios
          I want to append actions before the feature, before each scenario, after each scenario and after the feature.

          Actions Before the Feature:
            Given wait 3 seconds
            And waitrty 3 seconds
            And wait 3 seconds
            And step with a table
              | parameter     | value       |
              | sub_fields_1  | sub_value 1 |
              | sub_fields_2  | sub_value 2 |

          Actions Before each Scenario:
            Given the user navigates to the "www.google.es" url
            When the user logs in with username and password
            And wait 1 seconds
            And wait 1 seconds

          Actions After each Scenario:
            And wait 2 seconds
            And wait 2 seconds

          Actions After the Feature:
            And wait 4 seconds
            And step with another step executed dynamically
            And wait 4 seconds


All steps type are allowed:
   - with tables
   - executing another step internally

And in case that a step has failed a exception is threw, i.e. 'waitrty 3 seconds' step

Lettuce
~~~~~~~

Lettuce tests should be developed as usual, only *terrain.py* file should be modified to initialize driver and the rest
of Toolium configuration.

Terrain methods should call to the corresponding Toolium terrain methods, as can be seen in the following example:

.. code-block:: python

    from lettuce import after, before
    from toolium.lettuce.terrain import (setup_driver as toolium_setup_driver, teardown_driver as toolium_teardown_driver,
                                         teardown_driver_all as toolium_teardown_driver_all)


    @before.each_scenario
    def setup_driver(scenario):
        toolium_setup_driver(scenario)


    @after.each_scenario
    def teardown_driver(scenario):
        toolium_teardown_driver(scenario)


    @after.all
    def teardown_driver_all(total):
        toolium_teardown_driver_all(total)


After initialization, the following attributes will be available in world object:

- world.toolium_config: dictionary with Toolium configuration, readed from properties.cfg
- world.driver_wrapper: :ref:`DriverWrapper <driver_wrapper>` instance
- world.driver: Selenium or Appium driver instance
- world.utils: :ref:`Utils <utils>` instance
