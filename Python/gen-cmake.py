#!/usr/local/bin/python3
import sys
import os.path
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(
    usage="gen-cmake.py [options]",
    description="Generate a CMakeLists.txt file with libraries from the vcpkg toolchain",
    epilog="Note: if a CMakeLists.txt already exists in the specified directory, it will be rewritten",
    formatter_class=RawTextHelpFormatter
)
parser.add_argument(  "-d",  "--directory", default=".", type=str, help="Specify the directory of the generated CMakeLists.txt file (default: \".\")", metavar="")
parser.add_argument(  "-n",  "--name", default="Placeholder", type=str, help="Specify the name of the project (default: \"Placeholder\")", metavar="")
parser.add_argument(  "-la", "--language", default="c++", type=str, help="Specify the main programming language used (C, C++, or Fortran) (default: c++)", metavar="")
parser.add_argument(  "-c",  "--compiler", type=str, help="(Windows only) Specify the compiler to be used (msvc, gcc, clang, or Intel icx)", metavar="")
parser.add_argument(  "-l",  "--libs", nargs='+', type=str, help="Specify the libraries in vcpkg to be used\ncurrent libraries available:\n\t- glfw\n\t- glew\n\t- glm\n\t- cglm\n\t- imgui", metavar="")
parser.add_argument(  "-w",  "--Win32", help="(Windows only) Specify if the application uses the Win32 API", action="store_true")
parser.add_argument( "-rc",  "--resource", help="(Windows only) Specify if a resource file is to be used", action="store_true")
parser.add_argument("-osx",  "--osx-target", default="13", type=str, help="(macOS only) Specify the OSX deployment target (default: 13)", metavar="")
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
# print(args)
# print("----------")
if os.path.isfile("./CmakeLists.txt"):
    valid = False
    Query = input("A CmakeLists.txt file already exists, continuing will overwrite it.\nAre you sure you want to continue? (y/n): ")
    while valid is False:
        if Query.lower() == 'n' or Query.lower() == "no":
            sys.exit()
        elif Query.lower() == 'y' or Query.lower() == "yes":
            valid = True
        else:
            print("\nInvalid input.")
            Query = input("Are you sure you want to overwrite the current CmakeLists.txt? (y/n): ")


if args.Win32:
    print("Removing all non-Windows related content and commands.")

lang = None
Fortran = False
if args.language:
    match args.language:
        case "c" | "C":
            lang = args.language
        
        case "c++" | "C++" | "cpp" | "CPP" | "cxx" | "CXX":
            lang = args.language
        
        case "f" | "F" | "fortran" | "FORTRAN" | "Fortran" | "f90" | "f95" | "For" | "for":
            lang = args.language
            Fortran = True

        case _:
            print("Unknown language")
            lang = ""

with open(f"{args.directory}/CmakeLists.txt", "w") as file:
    file.write(
f"""# Made with gen-cmake.py
cmake_minimum_required (VERSION 3.8)

set(CMAKE_EXPORT_COMPILE_COMMANDS 1)
if (WIN32)
""")
    
    match args.compiler:
        case "msvc" | "cl":
            file.write("""    set(CMAKE_C_COMPILER MSVC)
    set(CMAKE_CXX_COMPILER MSVC)
""")
        case "gcc" | "g++":
            file.write("""    set(CMAKE_C_COMPILER gcc)
    set(CMAKE_CXX_COMPILER g++)
""")
        case "clang" | "clang++":
            file.write("""    set(CMAKE_C_COMPILER clang)
    set(CMAKE_CXX_COMPILER clang++)
""")
        case "icx" | "ifx" | "intel":
            file.write("""    set(CMAKE_C_COMPILER icx)
    set(CMAKE_CXX_COMPILER icx)
""")
        case _:
            if args.compiler != None:
                print("Warning: unknown compiler name specified")
    
    file.write("set(CMAKE_FC_COMPILER ifx)\n"
               if args.compiler == "icx"
               or args.compiler == "ifx"
               or args.compiler == "intel"
               else "set(CMAKE_FC_COMPILER gfortran)\n"
              )

    file.write("""elseif (APPLE)
    set(CMAKE_C_COMPILER clang)
    set(CMAKE_CXX_COMPILER clang++)
    set(CMAKE_FC_COMPILER gfortran)
endif()
""")
    file.write("#enable_language(Fortran)\n" if Fortran is True else "\n")
    file.write("""
if (CMAKE_C_COMPILER MATCHES icx)
    set(CMAKE_C_FLAGS "/std=c17")
    set(CMAKE_CXX_FLAGS "/Qstd=c++17")
endif()

cmake_path(SET ONEDRIVE $ENV{ONEDRIVE})
include_directories("${ONEDRIVE}/dev")

""")
    
    if args.libs != None:
        file.write("""cmake_path(SET ONEDRIVE $ENV{ONEDRIVE}) #because Windows and backslashes
if (WIN32)
    set(VCPKG_TARGET_TRIPLET x64-windows-static)
    set(CMAKE_TOOLCHAIN _FILE $C:/dev/libs/vcpkg/scripts/buildsystems/vcpkg.cmake)
elseif (APPLE)
    set(CMAKE_OSX_DEPLOYMENT_TARGET {args.osx_target})
    if (CMAKE_OSX_DEPLOYMENT_TARGET EQUAL 11)
        set(VCPKG_TARGET_TRIPLET x64-osx11-static)
    else()
        set(VCPKG_TARGET_TRIPLET x64-osx-static)
    endif()
    set(CMAKE_TOOLCHAIN _FILE ~/dev/libs/vcpkg/scripts/buildsystems/vcpkg.cmake)
endif()

""")
    
    
    file.write(f"project(\"{args.name}\")\n\n")
    
    file.write(f"add_executable(${{PROJECT_NAME}}{' WIN32' if args.Win32 else ''} \"{args.name}.{lang}\")\n\n")

    if args.resource:
        file.write("target_sources(${PROJECT_NAME} PRIVATE resource.rc)\n\n")

    file.write("""target_include_directories(${PROJECT_NAME} PRIVATE "${ONEDRIVE}/dev")

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD 20)
endif()

""")


    if args.libs != None:
        for lib in args.libs:
            if "glew" == lib.lower():
                file.write("""find_package(GLEW REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE GLEW::GLEW)

""")

            if "glfw" == lib.lower() or "glfw3" in lib.lower():
                file.write("""find_package(glfw3 CONFIG REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE glfw)

""")
                
            if "imgui" in lib.lower():
                file.write("""find_package(imgui CONFIG REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE imgui::imgui)

""")
                
            if "glm" == lib.lower():
                file.write("""find_package(glm CONFIG REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE glm::glm)

""")
                
            if "cglm" == lib.lower():
                file.write("""find_package(cglm CONFIG REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE cglm::cglm)

""")

# with open(f"{args.directory}/CmakeLists.txt", "r") as file:
#     print(file.read())
