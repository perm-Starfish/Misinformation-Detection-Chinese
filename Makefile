main: main.cpp utils.hpp
	g++ -std=c++11 -L./lib -I./include -o main main.cpp -lcurl -lgumbo -lgq

bonus: bonus.cpp utils.hpp
	g++ -std=c++11 -L./lib -I./include -o bonus bonus.cpp -lcurl -lgumbo -lgq

.PHONY=run
run: main
	LD_LIBRARY_PATH=${PWD}/lib ./main

runbonus: bonus
	LD_LIBRARY_PATH=${PWD}/lib ./bonus