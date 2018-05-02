# BIGSEA Asperathos - Monitor

## Overview
On the process of executing an application, the monitor service is responsible for managing all the needed steps to gather metrics from the application and/or its infrastructure and publish it in storage located in the cloud monitoring service (in our case, Monasca). The goal of this metric translation is to enable other components in the framework (e.g., the controller) to be generic, while still being able to process QoS metrics for the application and take decisions based on these metrics.

## Requirements
* Python 2.7 or Python 3.5
* Linux packages: python-dev and python-pip
* Python packages: setuptools, tox and flake8

To **apt** distros, you can use [pre-install.sh](https://github.com/bigsea-ufcg/bigsea-monitor/tree/refactor/tools/pre-install.sh) to install the requirements.

## Install
First of all, install **git**. After, you just need to clone the [Monitor repository](https://github.com/bigsea-ufcg/bigsea-monitor.git) in your machine.

### Configuration
A configuration file is required to run the Monitor. Edit and fill your monitor.cfg in the root of Monitor directory. Make sure you have fill up all fields before run.
You can find a template in [config-example.md](https://github.com/bigsea-ufcg/bigsea-monitor/tree/refactor/docs/config-example.md). 

### Run
In the Monitor directory, start the service using tox command:
```
$ tox -e venv -- monitor
```

## Avaliable plugins
* [Spark Sahara](https://github.com/bigsea-ufcg/bigsea-monitor/tree/refactor/docs/plugins/spark_sahara.md)
* [Spark Mesos](https://github.com/bigsea-ufcg/bigsea-monitor/tree/refactor/docs/plugins/spark_mesos.md)
* [Openstack Generic](https://github.com/bigsea-ufcg/bigsea-monitor/tree/refactor/docs/plugins/openstack_generic.md)
* [Web Application](https://github.com/bigsea-ufcg/bigsea-monitor/tree/refactor/docs/plugins/web_app.md)

## Monitor REST API
Endpoints is avaliable on [restapi-endpoints.md](https://github.com/bigsea-ufcg/bigsea-monitor/tree/refactor/docs/restapi-endpoints.md) documentation.

## Plugin development
See [plugin-development.md](https://github.com/bigsea-ufcg/bigsea-monitor/tree/refactor/docs/plugin-development.md).
