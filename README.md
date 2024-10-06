# MyCityDigitalTwin

**MyCityDigitalTwin** is a pipeline of scripts designed to simulate traffic in a 3D environment. The project leverages existing code, modified in some instances to add new features.

## Table of Contents
- [Installation](#installation)
- [Description](#description)
- [Contributing](#contributing)
- [License](#license)

## Installation

> **Important:**  
> This guide assumes you're working on a Windows PC.

Before proceeding, make sure to download and install the following dependencies:

- [**CARLA**](https://carla.readthedocs.io/en/latest/download/)
- [**SUMO**](https://sumo.dlr.de/docs/Downloads.php)
- [**Conda**](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

To set up the Conda environment using the provided `.yml` file, open the terminal and run:

```bash
conda env create -f environment.yml
```

> [!WARNING]
> It's important to add that there are different ways to download **CARLA** on your environment.<br/>
> It's highly recommended to download the **developer version**, even if it's the longest and more burdensome one on the PC. Using this version, let the user employ directly all the scripts already developed by **CARLA**'s devs. <br/>
> The **directory version** is way less burdensome but it may returns errors and the user would need to use third-party software, like the [**osm2xodr**](https://github.com/JHMeusener/osm2xodr) library to convert a osm file in a xodr.<br/>
> **In this guide, the latter will be assumed to be downloaded**

Once **CARLA** and the **conda env** are properly set, the repository is usable. There are two file that needs to be modified or moved:
1. **Move** the run_syncro.py script from the *Co-Simulation-Sumo* folder to the **CARLA** directory just downloaded: the path is something like CARLA_x.x.x/Co-Simulation/Sumo. <br/>
This scipt is to be used instead of the already developed run_synchronization.py in that folder.
2. [Not necessary] **Modify** the camera_with_tk.py script in the *camera* folder so that the path saved in the variable `json_file_path` is the absolute path to the run_syncro.py script just moved.

# Description

This section provides a step-by-step guide to creating a traffic digital twin of your city.

1. Go to [OpenStreetMap](https://www.openstreetmap.org/), navigate to the **Export** tab, and select an appropriate area to work with. Ensure the selected area is not too large, as this could lead to performance issues when using the 3D model.

2. Convert the downloaded *OSM* file into an *XODR* file. There are two ways to perform this conversion depending on your **CARLA** installation:
    - If you installed the **developer version** of CARLA, use the `osm_to_xodr.py` script located in the `carla-dev/PythonAPI/util` folder:
      ```bash
      python osm_to_xodr.py -i OSM_FILE_PATH -o XODR_FILE_PATH --traffic-lights --center-map
      ```
      If this returns an error, proceed with the next method.
    - If you installed the **CARLA folder** version, the `osm_to_xodr.py` script might cause errors. In that case, it's recommended to use a third-party library such as [osm2xodr](https://github.com/JHMeusener/osm2xodr), developed by **JHMeusener**.

3. Once the *XODR* file is generated, it is advisable to verify its correctness. Here are two methods to check the result:
    - Use the `validateXML.py` script found in the **UTILS** folder. This can help identify potential syntax errors in the file (e.g., symbols like `&`, which are harmless in OSM but problematic in XODR).
    - Use [odrviewer](https://odrviewer.io/), a software tool that allows you to visualize the 3D road network from the generated XODR file. The web page also links to the creator's GitHub repository.

   If the XODR file is valid, you have two options:
    - Proceed with a basic **CARLA** simulation using only the road network (skip to step #NUMERO).
    - Optionally, you can create a more detailed model that includes city buildings.

4. Explanation of using **Blender** and **UE4 Editor** for adding city structures.

5. Now that the **CARLA** part is done, focus on **SUMO**. You need to set up a configuration file (the `.sumocfg` file included in this repository). The `.sumocfg` file references four other files:
    - `viewsettings.xml` and `carlavtypes.rou.xml`, located in the `carlaUtils` folder—these files do not need any changes.
    - **Net file**: To generate this, navigate to the `CARLA_x.x.x/Co-Simulation/Sumo/util` directory and run the following command:
      ```bash
      netconvert_carla.py --output OUTPUT_PATH XODR_FILE_PATH
      ```
      Move the generated file to the same directory as the `.sumocfg` file or another accessible location.

    - **Traffic file**: Traffic generation in this project is random, but you can use **SUMO**'s `randomTrips.py` script to generate traffic patterns:
      ```bash
      python randomTrips.py -n yourCity.net.xml -r yourGeneratedTraffic.rou.xml --end N --insertion-density N
      ```
      After that, use the `modifyXML.py` script to assign the appropriate vehicle types:
      ```bash
      python modifyXML.py --xml yourGeneratedTraffic.rou.xml
      ```
      This will create a new file, `modified_yourGeneratedTraffic.rou.xml`, which can be referenced in the `.sumocfg` file.

6. With everything set up, it's time to start the co-simulation. First, open the **Conda** terminal, activate the environment, and navigate to the **CARLA** installation folder.  
   To launch a **CARLA** server, run:
   ```bash
   CarlaUE4.exe [--dx11] [--quality-level=Low] path/to/Carla/map
   ```
   This script has many useful functions, so it's recommended to explore them.

   Once the map is loaded into **CARLA**, the co-simulation can begin. From the **conda** terminal, navigate to `CARLA_x.x.x/Co-Simulation/Sumo` and run the following command:

    ```bash
    python run_syncro.py --tls-manager sumo --sync-vehicle-all --sumo-gui --debug "path/to/file.sumocfg"
    ```
    This command opens a **SUMO** GUI displaying the road network. From the GUI, you can adjust additional settings. Once everything is ready, press the start button on the GUI to begin the simulation.

7. Once the co-simulation is running, several options are available:
    
    - Use two different camera scripts to follow vehicles in the simulation. The `camera.py` script randomly follows vehicles each time the ENTER key is pressed. The other script requires an input parameter `--id`, which follows a specific vehicle,             displaying basic info in a Tkinter widget.
    
    - Open the interface to monitor all vehicles in the simulation. From the conda terminal, navigate to the interface folder and run:
    
    ```bash
    streamlit run interface.py
    ```
    This will open your default browser and show a locally hosted app where you can monitor detailed information about the ongoing simulation.


# Contributing
In this section, all the already-developed software used in this project will be listed:
- [CARLA 0.9.15](https://carla.org/2023/11/10/release-0.9.15/)
- [sumo 1.20](https://sumo.dlr.de/docs/Downloads.php)
- [miniconda](https://docs.anaconda.com/miniconda/)
- [osm2xodr](https://github.com/JHMeusener/osm2xodr)
- [odrviewer](https://odrviewer.io/)


# License
This is a open-source project for a university project, so it's ok to use this code however needed, just look up for the licence of every already-developed software used.
    
     
                  
     
     
      
      
   
   
      
   





