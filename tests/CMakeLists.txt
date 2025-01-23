## We want to add all of our tests to a custom target and exclude them from "make all" so that
## testing can be built and run optionally. The "make test" target will run the unit tests, but not 
## compile the tests themselves. We create the target SHARPlib_tests so that all unit tests can be
## aggregated under a single build command.
add_custom_target(NFDRS4_tests)


## Create an executable with the given name from the given source, excluding
## it from the "make all" target. Then link it to the base static library,
## and then add a test to CTests
add_executable(test_nfdrs4 EXCLUDE_FROM_ALL test_nfdrs4.cpp)
target_link_libraries(test_nfdrs4 NFDRS4) 
include_directories(./ ${CMAKE_SOURCE_DIR}/lib/NFDRS4/include)
add_test(NAME nfdrs4_test COMMAND test_nfdrs4)


## This aggregates all of the executable names into a single 
## target for building and testing
add_dependencies(NFDRS4_tests test_nfdrs4)
