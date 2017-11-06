OBJS = common.o build_model.o data_IO.o Osiris_train.o event_detection.o event_handling.o Osiris.o
CC = gcc
CXX = g++
DEBUG = -g
LIBFLAGS = -L Penthus/ -l Penthus -fopenmp
CXXFLAGS = -Wall -c -O2 -std=c++11 -fopenmp $(DEBUG)
CFLAGS = -Wall -c -O2 $(DEBUG)
LFLAGS = -Wall -O2 $(DEBUG)


MAIN_EXECUTABLE = bin/Osiris

$(MAIN_EXECUTABLE) : $(OBJS)
	$(CXX) $(LFLAGS) $(OBJS) -o bin/Osiris $(LIBFLAGS)

event_detection.o : src/scrappie/event_detection.h
	$(CC) $(CFLAGS) src/scrappie/event_detection.c

event_handling.o : src/event_handling.h src/poreModels.h
	$(CXX) $(CXXFLAGS) src/event_handling.cpp

common.o : src/common.h src/common.cpp
	$(CXX) $(CXXFLAGS) src/common.cpp $(LIBFLAGS)

data_IO.o : src/data_IO.h src/data_IO.cpp
	$(CXX) $(CXXFLAGS) src/data_IO.cpp $(LIBFLAGS)

build_model.o : src/build_model.h src/build_model.cpp src/data_IO.h src/poreModels.h
	$(CXX) $(CXXFLAGS) src/build_model.cpp $(LIBFLAGS)

Osiris_train.o : src/event_handling.h src/Osiris_train.h src/Osiris_train.cpp src/data_IO.h src/build_model.h src/common.h src/event_handling.h src/poreModels.h
	$(CXX) $(CXXFLAGS) src/Osiris_train.cpp $(LIBFLAGS)

Osiris.o : src/Osiris.cpp src/Osiris_train.h src/Osiris_fixedPos.h src/data_IO.h src/build_model.h src/event_handling.h
	$(CXX) $(CXXFLAGS) src/Osiris.cpp $(LIBFLAGS)

clean:
	rm $(OBJS) $(MAIN_EXECUTABLE)
