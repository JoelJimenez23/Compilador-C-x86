cmake_minimum_required(VERSION 3.10)
project(C_x86_compiler)


set(HEADER_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include)
add_executable(compiler
	main.cpp
	src/ast.cpp
	src/parser.cpp
	src/token.cpp
	src/visitor.cpp
	src/scanner.cpp
)
target_include_directories(compiler
	PRIVATE
	${HEADER_DIR}
)
