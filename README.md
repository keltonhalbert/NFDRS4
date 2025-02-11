# NOAA / NWS / NCEP Storm Prediction Center Fork of NFDRS4
This is a fork of the NFDRS4 repository from the FireLab GitHub repository. While there are ongoing efforts to test, refactor, and baseline NFDRS4 into SPC postprocessing workflows, some documetnation, code, and features may not be up to date. Changes have been made from the original repository to better facilitate building and testing. The build instructions will be kept up to date, but while things are in flux, there may be discrepencies in other areas. 

# NFDRS4 - National Fire Danger Rating System 4.0
The repository houses the source code for the US National Fire Danger Rating System Version 4.0.
The source code provides access to the Command Line Interface as well as SWIG wrappers to build Python libraries.  It also provides documentation on the formats of the inputs for the CLI was well as an FW13 to FW21 weather data file converter.

The model documentation can be found here:
[Modernizing the US National Fire Danger Rating System (version 4): Simplified fuel models and improved live and dead fuel moisture calculations](https://www.sciencedirect.com/science/article/pii/S1364815224002421)

## Multiplatform source for NFDRS4 static library
This library provides all of the source code for NFDRS Version 4.0 including the Nelson Dead Fuel Moisture Model, the Growing Season Index-based Live Fuel Moisture Model and the NFDRS calculator.

Also produces two apps: the FireWxConverter and the NFDRS4_cli (command line interface). 

FireWxConverter, which converts FW13 fire weather data files to FW21 fire weather data files
NFDRS4_cli produces live and dead fuel moistures as well as NFDRS indexes from FW21 fire weather data files.

### Dependencies:

*CMAKE NFDRS4* - requires CMAKE version 3.8 or higher

*Config4cpp* - see http://www.config4star.org/
 Config4cpp is used by NFDRS4 for defining configuration files for NFDRS4_cli and NFDRS4 initialization (station) parameters. 
 Complete source for config4cpp is included in the 'extern' directory. Previously, an additional manual build step was required, but CMake integration was added as part of the SPC fork. No user configuration or intervention is necessary.

*utctime* - see http://paulgriffiths.github.io/utctime/documentation/index.html
 UTCTime class is used for handling time in NFDRS4. Complete source is in the lib/utctime directory

License - NFDRS4 is public domain software, still under development at this time.

## Building in MS Windows
### ***NOTE:*** This information may not be up to date, as windows build have not been tested in the current state of the fork/refactor. The legacy instructions have been left alone, but may not be valid. 


Building for MS Windows has been tested with MS Visual Studio 2022
*Steps*<br>
*Build config4cpp*<br>
Build config4cpp.lib is easiest accomplished by use of the x64 Native Tools Command Prompt for VS 2022.<br>
Open the x64 Native Tools Command Prompt for VS 2022, navigate to the NFDRS4/extern/config4cpp directory and enter: ```nmake -f Makefile.win all64```<br> 
This should produce config4cpp.lib static library in NFDRS4/extern/config4cpp/lib<br><br>
Navigate back to the root NFDRS4 directory<br>
Run ```cmake -G "NMake Makefiles" .```<br>
*If you haven't already done so, edit the entries for CONFIG4CPP_DIR and CONFIG4CPP_LIB in CMakeCache.txt*<br>
Example:<br>
//Path to a file.<br>
CONFIG4CPP_DIR:PATH=S:/src/NFDRS4/extern/config4cpp/include<br>

//Path to a library.<br>
CONFIG4CPP_LIB:FILEPATH=S:/src/NFDRS4/extern/config4cpp/lib/config4cpp.lib*<br>

Rerun ```cmake -G "NMake Makefiles" .```, there should be no errors<br>
Run ```nmake```<br><br>

## Build NFDRS4 from Visual Studio 2022
### ***NOTE:*** This information may not be up to date, as VSCode/Studio builds have not been tested in the current state of the fork/refactor. The legacy instructions have been left alone, but may not be valid. 
In Visual Studio 2022, open the NFDRS4 folder and NFDRS4 will load as a CMake project<br>
Select Project - CMake Settings for NFDRS4<br>
Create a Configuration for x64-Release<br>
Save the settings, Cmake will run
~~Populate the entry in CMakeSettings.json for CONFIG4CPP_DIR 
	(should be <repo location>/NFDRS4/extern/config4cpp/include where <repo location> is the Drive and folder where the NFDRS4 repository is located)
	e.g. D:/Repos/NFDRS4/extern/config4cpp/include
Populate the entry in CmakeSettings.json for CONFIG4CPP_LIB
	(should be <repo location>/NFDRS4/extern/config4cpp/lib/config4cpp.lib)
	e.g. D:/Repos/NFDRS4/extern/config4cpp/lib/config4cpp.lib
Save CMakeSettings.json, CMake will run and there should be no errors~~

Select Build - Build All
Select Build - Install NFDRS4
	- this will create an install folder for X64-Release with necessary include and lib files to use NFDRS4 and fw21 with applications, as well as executables
	NFDRS4_cli.exe and FireWxConverter.exe

## Building NFDRS4 for Linux
Building NFDRS4_cli and the static library from the project root directory:
```bash
cmake -B build .
cmake --build build -j {N_JOBS}
```
where ```{N_JOBS}``` should be a number representing the number of parallel build processes.

