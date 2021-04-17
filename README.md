# V2V-ML

## Cryptography Class Project - Spring 2021

## Team Members
- Christian Bargraser
- Brenna Lusk
- Brent Tuttrup
- Zachary Vater

## Purpose
Node classification in V2V systems with machine learning.

## Inspiration
Each group picked a paper from a list of 10 papers. The paper we chose was **TangleCV: A Distributed Ledger Technique for Secure Message Sharing in Connected Vehicles** by Dr. Rathore, Dr. Samant, and Dr. Jadliwala. In the paper, nodes are able to determine the trustworthiness of other nodes through the use of a Distributed Acyclic Graph (DAG). 

Instead of using a DAG to determine a node's trustworthiness, our project aims to allow nodes to independently classify nodes as _good_, _faulty_, or _malicious_ through the use of machine learning. 

# BSM messages
According to **TangleCV: A Distributed Ledger Technique for Secure Message Sharing in Connected Vehicles**, nodes broadcast BSM messages every epoch, or 100 ms. In our project, we simulate the coordinates reported by BSM messages selecting some random error for each of a node's actual coordinates. Each node type has a maximum possible error.


## Requirements
- PyCharm IDE
- Anaconda, includes necessary libariess:
  - Numpy
  - Pandas
  - SciKit Learn
  - Seaborn
  - TKinter

## Installation

1) Download the code
2) Open the project in PyCharm
3) Select the interpreter of your choice
4) Set the mode in the configuration file
5) Modify other settings in the configuration file
6) Run program

## Modes

Program behavior is determined by the mode set by the MODE variable in the configuration file.



## Mode Descriptions - _High Level_
- MODE_GATHER_DATA
  - The simulation is run for _n_ epochs. A node's actual coordinates and BSM reported coordinates are written out to a file.


- MODE_EXTRACT_FEATURES
  - Features are extracted from the data recorded from MODE_GATHER_DATA.


- MODE_TEST_MODELS
  - Using the features extracted from MODE_EXTRACT_FEATURES, machine learning algorithms are trained and run _n_ times. Statistics are output to the console.


- MODE_EXPORT_MODELS
  - Using the features collected in MODE_EXTRACT_FEATURES, models are trained only once and saved to a _.pkl_ file


- MODE_VISUALIZE
  - Visualizes the simulation the simulation that is used in MODE_GATHER_DATA. 


- MODE_PLOTS
  - Generates graphs and plots for the statistics output from MODE_TEST_MODELS. The output from MODE_TEST_MODELS.


## Running the GUI

Set the MODE variable in the configuration file equal to MODE_VISUALIZE


## GUI Features

Enable and disable features using the toolbar at the bottom of the GUI. 
Features include:
- Auto
  - Automatically advances to the next epoch after SIM_EPOCH_WAIT_TIME seconds.
  - Unchecking this feature will put the simulation in manual mode.
    - Clicking the left mouse button will advance to the next button.
    - Clicking on a node with the right button will show node details in a pop-up window.


- On/Off
  - Toggles all features on or off (except for the auto feature).
 

- Node Type
  - When off, all nodes are black. 
  - When on:
    - _good_ nodes are green
    - _faulty_ nodes are yellow
    - _malicious_ nodes are purple.


- Node History
  - Show the previous _n_ coordinates where a node has been, where _n_ is specified by MAX_COORD_HIST


- Outer Radius
  - Draw a circle represeting the area covered by a node's sensors.


- Inner Radius
  - Draw a circle representing the area in which node's can detect each other and verify each other's presence.


- Outer Connect
  - Draw a line connecting nodes when their outer circles overlap, showing that nodes can exchange messages.


- Inner Connect
  - Draw a line connectiing nodes when their inner circles overlap, showing that they can verify each other's coordinates.


- BSM History
  - Show the previous _n_ BSM coordinates reported by a node, where _n_ is specified by MAX_BSM_HIST


## Running the ML Parts

- Get model statistics
  - 1. Run the progrma in MODE_GATHER_DATA
  - 2. Run the program in MODE_EXTRACT_FEATURES
  - 3. Run the program in MODE_TEST_MODELS

- Save models to files
  - 1. Run the progrma in MODE_GATHER_DATA
  - 2. Run the program in MODE_EXTRACT_FEATURES
  - 3. Run the progrma in MODE_EXPORT_MODELS


- Get model plots
  - 1. Run the progrma in MODE_GATHER_DATA
  - 2. Run the program in MODE_EXTRACT_FEATURES
  - 3. Run the program in MODE_TEST_MODELS
  - 4. Run the program in MODE_PLOTS


## Mode Descriptions - _Low Level_

- MODE_GATHER_DATA
  - The simulation will be run _n_ times, where _n_ is specified in the configuration file by _GATHER_DATA_NUM_EPOCHS_.
  - Each node that enters the simulation creates its own _.csv_ file named _node##.csv_
  - _good_ nodes save their data to _./data/raw\_data/good_
  - _faulty_ nodes save their data to _./data/raw\_data/faulty_
  - _malicious_ nodes save their data to _./data/raw\_data/malicious_


- MODE_EXTRACT_FEATURES
  - For each _.csv_ file in _./data/raw\_data/good_, features are extracted and saved to a _.csv_  in _./data/processed\_data/_. An extra ',0' is added to the end of each line.
  - For each _.csv_ file in _.data/raw\_data/faulty_, features are extracted and saved to a _.csv_ in _./data/processed\_data/_. An extra ',1' is added to the end of each line.
  - For each _.csv_ file in _.data/raw\_data/malicious_, features are extracted and saved to a _.csv_ in _./data/processed\_data/_. An extra ',2' is added to the end of each line.


- MODE_TEST_MODELS
  - Each _.csv_ file in _./data/processed\_data/_ is loaded into a DataFrame. Each DataFrame is saved into a list. Inside of a loop that runs _n_ times, _test_train_split()_ is called, models are trained, and then tested.
  - _n_ is specified by TRAIN_MODELS_NUM_TESTS in the configuration file.
  - We then:
    - Take the average accuracy of _n_ runs
    - Produce the average classification report
    - Find what each samples was labelled as, as recall and precision alone do not show what samples are actually being incorrectly being labelled as.


- MODE_EXPORT_MODELS
  - Each _.csv_ file in _./data/processed\_data/_ is loaded into a DataFrame. Each DataFrame is saved into a list. _test_train_split()_ is called once. The models are then trained and saved to _.pkl_ files using _pickle.dump()_.



- MODE_VISUALIZE
  - Graphically displays the simulation after each epoch. Features can be enabled and disabled using the toolbar at the bottom. 


- MODE_PLOTS
  - Create a lineplot showing how the average model accuracy increases as sample size increases.
  - Create catplots showing what percentage of _good_, _faulty_, and _malicious_ nodes were labelled as for sample sizes _n=3_, _n=6_, and _n=10_. In other words:
    - For _good_ nodes, show what percentage of _good_ nodes were labelled as _good_, _faulty_, and _malicious_ for _n=3_, _n=6_, and _n=10_.
    - For _faulty_ nodes, show what percentage of _faulty_ nodes were labelled as _good_, _faulty_, and _malicious_ for _n=3_, _n=6_, and _n=10_.
    - For _malicious_ nodes, show what percentage of _malicious_ nodes were labelled as _good_, _faulty_, and _malicious_ for _n=3_, _n=6_, and _n=10_.


## Features

- Feature 1: Average Distance
  - The average distance between a node's actual coordinates their corresonding BSM coordinates.

- Feature 2: Average Ratio
  - Average ratio of the lengths of segments formed by a node's actual coordintes and the segments formed by BSM coordinates. 

- Feature 3: Average Angle
  - The average angle formed by BSM points.

- Feature 4: Slope
  - The slope of the best fit line for the BSM points.
  - If a node is heading north or south, the _x_ and _y_ coordinates for the BSM points are swapped prior to calculating the slope. 

- Feature 5: Average Dif
  - The average difference between the _x_ and _y_ values of a node's actual coordinates and BSM coordinates. 
