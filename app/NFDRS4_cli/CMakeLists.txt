cmake_minimum_required(VERSION 3.13)
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

project(NFDRS4_cli)

IF(MSVC)
	add_compile_definitions(_CRT_SECURE_NO_WARNINGS)
ENDIF(MSVC)

set(BUILD_SHARED_LIBS OFF CACHE BOOL "Build static libraries" FORCE)
include_directories(${CMAKE_SOURCE_DIR}/extern/config4cpp/include)

add_executable(
    ${PROJECT_NAME} 
    src/CNFDRSParams.cpp 
    src/NFDRSConfiguration.cpp 
    src/NFDRSInitConfig.cpp 
    src/RunNFDRS.cpp 
    src/RunNFDRSConfig.cpp 
    src/RunNFDRSConfiguration.cpp
)

target_link_libraries (${PROJECT_NAME} PUBLIC NFDRS4 fw21 PRIVATE config4cpp)
