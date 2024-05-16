# eq
## Overview

This repository contains the core drivers and logic for the sensors and lights used in our workout product. It also includes the code required to support multiple workout modes, ensuring a versatile and customizable workout experience.

### Features
- Sensor Drivers: Includes drivers for our filmsensors
- Light Drivers: Controls and manages the ws2812b led rings
- Workout Modes: Supports different workout modes 
- Extensible: Designed to be easily extendable with additional sensors and workout modes.

### Files
- filmsense.py: contains the code to poll from the film sensors

- ringctl.py: contains the code to control the ws2812b ledrings

- speed.py: contains an example implementation of one of our workout modes