# MyCityDigitalTwin

**MyCityDigitalTwin** is a *pipeline of scripts* that realize a traffic simulation in a 3D environment, made using already developed code modified in some instances to add some features.

# Table of Contents
- [Installation](#installation)
- [Description](#description)
- [Contributing](#contributing)
- [License](#license)

# Installation
 > [!IMPORTANT]
> In this page, we will discuss the process in a Windows PC.

 > [!IMPORTANT]
> Before starting to download and use this repository, it's mandatory to download [**CARLA**](https://carla.readthedocs.io/en/latest/download/), [**sumo**](https://sumo.dlr.de/docs/Downloads.php) and set up a [**conda environment**](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) using the *yml* file. Once the conda terminal is open: <br/><br/>
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
In this section, a guide to build a traffic digital twin of your city will be explained step by step.<br/><br/>
1. Go to [OpenStreetMap](https://www.openstreetmap.org/), go to the export tab and select a proper area to work with. Just make sure it's not to big, else it might create lag in the next steps where the  
   actual 3D model will be used.<br/>
   
2. Then convert the *osm* file in a *xodr* file. This operation can be done in 2 different ways depending on how **CARLA** was downloaded:
    - If you downloaded the devs' version, use the osm_to_xodr.py script in the *carla-dev\PythonAPI\util* folder.<br/>
      `python osm_to_xodr.py -i OSM_FILE_PATH  -o XODR_FILE_PATH  --traffic-lights  --center-map` <br/>
      In case this returns an error, just follow the other point.<br/>
    - If you downloaded the **CARLA** folder, the osm_to_xodr.py script may returns errors so it's recommended to use a different method for the conversion. For this application case, we advice an already- 
      developed python library, [osm2xodr](https://github.com/JHMeusener/osm2xodr), made by JHMeusenerbr. <br/>
 
3. Once the *xodr* file is obtained, it's highly recommeded to double-check the result. There are 2 simple ways:
    - Use the validateXML.py script in UTILS, and it could eventually find errors in the syntax of the file (there are simbols that are not critically damaging in a *osm* file, but they are in the *xodr*, 
      e.g. "&")
    - Use [odrviewer](https://odrviewer.io/), a software that let the user see a 3D version of the generated *xodr* file. From that web page, it's possible to reach the github page of the creator.
   If the *xodr* file is well formatted, there are 2 ways to procede: you can already do the **CARLA** simulation with just the road network (skip to step #NUMERO) or you can already build the city's  
   buildings.

4. SPIEGAZIONE DI BLENDER E DI UE4 EDITOR


5. Once you are done with this **CARLA**'s side of the creation phase, we need to focus on the **sumo**'s side. For **sumo**, you need to build a configuration file (the *sumocfg* in the repository). Opening this file, it's understandable that 2 more files are needed to compile a functioning code. There are **4 files** in the *config* file: the `viewsettings.xml` and the `carlavtypes.rou.xml`, both in the *carlaUtils* folder in this repository, no need to modify them, and then the **net** and the **traffic** file (in this project, `Bari.net.xml` and `modified_traffic.rou.xml`, respectively)
    - **Net file**: move to *CARLA_x.x.x\Co-Simulation\Sumo\util* directory and then use the command: <br/> `netconvert_carla.py --output OUTPUT xodr_file` <br/> Then move the result in the same directory  
      of the *sumocfg* file, or in an accessible directory from there.
    - **Traffic file**: There may be a logic behind the generation of the traffic in a given scenario, but in this case a random generation logic is adopted. <br/>
       The path's generation of each vehicle is done using a **sumo**'s script (it's recommended to use --help to see every option in this command): <br/>
      `python randomTrips.py -n yourCity.net.xml -r yourGeneratedTraffic.rou.xml --end N  --insertion-density N` <br/>
      Then, it's added to every vehicle the *type* attribute using the modifyXML.py script <br/>
      `python modifyXML.py  --xml yourGeneratedTraffic.rou.xml` <br/>
      This last script returns a new file, modified_yourGeneratedTraffic.rou.xml, that will be used in the *sumocfg* file.

  6. Once everything is done and functioning, it's time to start the co-simulation. First open the **conda** terminal, activate the environment and go to the **CARLA** downloaded folder. <br/>
     To start a **CARLA** server, use: <br/>
     `CarlaUE4.exe [--dx11] [--Graphic=Low] path/to/Carla/map` <br/>
     It's not necessary to specify now the path to the map that is going to use, but of course this speeds up the process. If the map was not specified, the config.py script in CARLA_x.x.x\PythonAPI\util 
     folder. This script is fundamental if the simulation is done only with the road network in *xodr* format. <br/>
     `python config.py [-m MAP] [--rendering] [--no-rendering] [--no-sync] [-i]  [-x XODR_FILE_PATH] [--osm-path OSM_FILE_PATH]` <br/>
     There are a lot of usefull functions in this script, so it's recommended to go look at them. <br/>
     Once the map is loaded in **CARLA**, the co-simulation can be initiated:
     From the **conda** terminal, move to CARLA_x.x.x\Co-Simulation\Sumo and then use:
     `python run_syncro.py --tls-manager sumo --sync-vehicle-all  --sumo-gui  --debug "path/to/file.sumocfg"` <br/>
     `--sync-vehicle-all` synchronize all vehicle properties (default: False)  `--tls-manager {none,sumo,carla}` select traffic light manager (default: none)<br/>
     `--debug`               enable debug messages
     
                  
     
     
      
      
   
   
      
   





