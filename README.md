# MyCityDigitalTwin

**MyCityDigitalTwin** is a *pipeline of scripts* that realize a traffic simulation in a 3D environment, made using already developed code modified in some instances to add some features.

# Table of Contents
- [Installation](#installation)
- [Description](#description)
- [Contributing](#contributing)
- [License](#license)

# Installation
 > [!IMPORTANT]
> Before starting to download and use this repository, it's mandatory to download [**CARLA**](https://carla.readthedocs.io/en/latest/download/) and set up a [**conda environment**](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) using the yml file. Once the conda terminal is open: <br/><br/>
>`conda env create -f environment.yml`

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
In this section, a guide to build a traffic digital twin of your city will be explained step by step.
1. Go to [OpenStreetMap](https://www.openstreetmap.org/) 





