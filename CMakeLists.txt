# CMakeList.txt : projet CMake pour CMake-VCPKG, incluez la source et définissez
# la logique spécifique au projet ici.
#
cmake_minimum_required (VERSION 3.8)

# Activez Rechargement à chaud pour les compilateurs MSVC si cela est pris en charge.
if (POLICY CMP0141)
  cmake_policy(SET CMP0141 NEW)
  set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>")
endif()

project ("CMake-VCPKG")
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CPM_DOWNLOAD_VERSION 0.42.0)
set(CPM_HASH_SUM "2020b4fc42dba44817983e06342e682ecfc3d2f484a581f11cc5731fbe4dce8a")

if(CPM_SOURCE_CACHE)
  set(CPM_DOWNLOAD_LOCATION "${CPM_SOURCE_CACHE}/cpm/CPM_${CPM_DOWNLOAD_VERSION}.cmake")
elseif(DEFINED ENV{CPM_SOURCE_CACHE})
  set(CPM_DOWNLOAD_LOCATION "$ENV{CPM_SOURCE_CACHE}/cpm/CPM_${CPM_DOWNLOAD_VERSION}.cmake")
else()
  set(CPM_DOWNLOAD_LOCATION "${CMAKE_BINARY_DIR}/cmake/CPM_${CPM_DOWNLOAD_VERSION}.cmake")
endif()

# Expand relative path. This is important if the provided path contains a tilde (~)
get_filename_component(CPM_DOWNLOAD_LOCATION ${CPM_DOWNLOAD_LOCATION} ABSOLUTE)

file(DOWNLOAD
     https://github.com/cpm-cmake/CPM.cmake/releases/download/v${CPM_DOWNLOAD_VERSION}/CPM.cmake
     ${CPM_DOWNLOAD_LOCATION} EXPECTED_HASH SHA256=${CPM_HASH_SUM}
)

include(${CPM_DOWNLOAD_LOCATION})

CPMAddPackage(
    NAME CATCH2
    GITHUB_REPOSITORY CatchOrg/Catch2
    VERSION 3.6.0
    OPTIONS "CATCH_BUILD_TESTING OFF"
)

CPMAddPackage(
    NAME SFML
    GITHUB_REPOSITORY SFML/SFML
    GIT_TAG 3.0.2
    OPTIONS
        "SFML_BUILD_EXAMPLES OFF"
        "SFML_BUILD_TEST_SUITE OFF"
        "SFML_BUILD_DOC OFF"
        "SFML_SHARED_LIBS ON"
        "CMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}"
        $<$<PLATFORM_ID:Windows>:"SFML_GENERATE_PDB ON">
        $<$<AND:$<PLATFORM_ID:Darwin>,$<CONFIG:Release>>:
            "CMAKE_INSTALL_PREFIX=/Library/Frameworks"
            "SFML_BUILD_FRAMEWORKS ON"
        >
        $<$<AND:$<PLATFORM_ID:Darwin>,$<CONFIG:Debug>>:
            "SFML_BUILD_FRAMEWORKS OFF"
        >
)

enable_testing()

# Ajoutez une source à l'exécutable de ce projet.
add_executable (CMake-VCPKG "main.cpp" "main.h")
target_link_libraries(CMake-VCPKG PRIVATE Catch2::Catch2)
target_link_libraries(CMake-VCPKG PRIVATE SFML::Network SFML::Graphics SFML::Window SFML::Audio SFML::System)

#find_package(SFML COMPONENTS Network Graphics Window Audio System CONFIG REQUIRED)
#target_link_libraries(main PRIVATE SFML::Network SFML::Graphics SFML::Window SFML::Audio SFML::System)

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET CMake-VCPKG PROPERTY CXX_STANDARD 20)
endif()

# TODO: Ajoutez des tests et installez des cibles si nécessaire.
