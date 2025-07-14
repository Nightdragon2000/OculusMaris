# Oculus Maris  

## Overview

**Oculus Maris** (*Latin: “Eye of the Sea”*) is an experimental system that blends real-time digital maritime data with a physical spatial interface. Built as part of a thesis project, it captures and decodes live AIS signals, visually projecting vessel positions onto a georeferenced model of the Cyclades archipelago.

Users interact with the system using natural hand gestures, tracked through a webcam, to explore ship data without physical contact. The architecture is modular and adaptable, allowing easy reconfiguration for other geographic locations or installations.

## Features

- Real-time AIS decoding and ship tracking
- Automatic metadata fetching (name, destination, ETA)
- Projection of live data onto a physical 3D maquette
- Gesture-based interaction via webcam (no touch needed)
- Projector and camera calibration tools
- Flexible georeferencing of custom map images
- Dual database support: PostgreSQL or MySQL
- Launcher interface with modular configuration


## Installation

### First-Time Setup
Run the setup script to prepare the Python environment:

```bat
first_time_setup.bat
```

This will:
- Create and activate a virtual environment
- Upgrade pip
- Install all required dependencies from requirements.txt

### Regular Use
Once the environment is installed and configured, Oculus Maris can be started using:

```bat
run.bat
```

This will activate the virtual environment and open the splash screen, followed by the main menu interface.

From the main menu, you can:

Run Main Application: Start the real-time vessel visualization and gesture-based interaction

Setup & Calibration: Access tools to:

- Calibrate projector alignment
- Define the camera tracking region
- Georeference a new map image
- Configure the database connection

Help: View in-app instructions and interaction tips

## Usage Guide

### Main Interface

After launching Oculus Maris, a splash screen will appear briefly with the system logo and version label. Once complete, the main graphical interface will open, providing access to all system modules.

From the main menu, you can:

- **Run Main Application**: Starts the real-time visualization system  
- **Setup & Calibration**: Opens tools to configure the environment  
- **Help**: Opens an integrated usage guide with system instructions  

When running the main application, the system will:
- Attempt to detect a connected AIS receiver
- If found, launch AIS decoding in a separate console window
- Prompt the user to select a projection monitor
- Begin displaying ships and enabling interaction via webcam gestures  

You may also choose to continue without live AIS input. In this case, the system operates in offline mode using cached data.

### Interaction

- **To select a ship**: Point your index finger and hover above the ship’s position for ~2 seconds  
- **To deselect a ship**: Perform a pinch gesture (index finger and thumb together)  
- When a ship is selected, a panel will display:
  - Ship image (if available)
  - Name
  - Destination
  - Estimated Time of Arrival (ETA)
  - Navigation status  

The camera tracking zone is defined during calibration and may be adjusted at any time through the configuration interface.


## System Requirements

To run Oculus Maris, the following system configuration is recommended:

- **Operating System**: Windows 10 or later  
- **Python**: Version 3.8 or newer  
- **Hardware**:
  - A webcam
  - A second monitor or projector
  - An AIS receiver connected via USB 
- **Database**:
  - PostgreSQL or MySQL server installed and accessible
  - A database and user credentials created prior to setup
