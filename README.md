# KX Problem solving exercise

## Problem
We would like you to implement a distributed **Service Assembly** with a gateway component.

## Description
The service assembly will have the following components:
1) **Storage Service** - stores in-memory, dummy data that can be accessed through a REST GET call in JSON format
2) **Gateway Service** - main process that serves data to clients and tracks the availability of the Storage Services (there could be 0 to 3 available) and has the following REST endpoints
    * **/status** - returns the status of each Storage Service
    * **/data** - fetches the dummy data from a Storage Service (eg. with round robin) and returns the data in JSON format

We would like the services to be containerised and run with docker-compose.
The services can be implemented using any programming language.

## Architecture
<img src="https://user-images.githubusercontent.com/90027208/152865747-5c4734dd-c046-4170-ae04-f0ea1448cf89.png" width="300">

## Acceptance criteria
* Please fork this git repository and work inside your own
* Provide a solution for the described problem and give us the instructions necessary to execute it
* We would like to have your solution in form of a Pull Request into the main repository
* _What should the Gateway do if no Storage Services are running?_
