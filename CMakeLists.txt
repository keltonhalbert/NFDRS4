cmake_minimum_required (VERSION 3.13)
set_property(GLOBAL PROPERTY USE_FOLDERS ON)
set(BUILD_SHARED_LIBS OFF CACHE BOOL "Build static libraries" FORCE)

project (
	NFDRS4
	VERSION 1.0
	DESCRIPTION "National Fire Danger Rating System 4"
	LANGUAGES CXX)

option(BUILD_CLI "Build the NFDRS4_CLI." OFF)

# Only do these if this is the main project, and not if it is included through add_subdirectory
if(CMAKE_PROJECT_NAME STREQUAL PROJECT_NAME)

  # Let's ensure -std=c++xx instead of -std=g++xx
  set(CMAKE_CXX_EXTENSIONS OFF)
  set(BUILD_CLI ON)

  # Let's nicely support folders in IDEs
  set_property(GLOBAL PROPERTY USE_FOLDERS ON)

endif()

add_subdirectory(lib)

#install locations for apps, headers, and libs
set(include_dest "include")
set(lib_dest "lib")

if (BUILD_CLI)
    add_subdirectory(app)
    add_subdirectory(extern/config4cpp)
    add_dependencies(NFDRS4_cli config4cpp-static)
    set(app_dest "bin")
endif()

