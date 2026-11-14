cmake_minimum_required(VERSION 3.20)
project(StormCore)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

add_executable(stormc 
    src/main.cpp
)

# TODO: Add Lexer.cpp, Parser.cpp when ready