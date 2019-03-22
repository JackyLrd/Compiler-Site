# DIR_INC = ./include
# DIR_SRC = ./src
# DIR_OBJ = ./obj
# DIR_BIN = ./bin
# COMPILE_OPT

SRC = $(wildcard ${DIR_SRC}/*.cpp)  
OBJ = $(patsubst %.cpp,${DIR_OBJ}/%.o,$(notdir ${SRC})) 

TARGET = target

BIN_TARGET = ${DIR_BIN}/${TARGET}

CC = clang++
CFLAGS = -g -Wall -I ${DIR_INC}
CFLAGS += $(COMPILE_OPT)

${BIN_TARGET}:${OBJ}
	@if [ ! -d $(DIR_BIN) ]; then mkdir -p $(DIR_BIN); fi;
	@if [ ! -d $(DIR_OBJ) ]; then mkdir -p $(DIR_OBJ); fi;
	@echo "start to link program"
	$(CC) $(OBJ) -o $@
	@echo "program linked"
    
${DIR_OBJ}/%.o:${DIR_SRC}/%.cpp
	@echo "start to compile $*.cpp"
	$(CC) $(CFLAGS) -c $< -o $@
	@echo "$*.cpp compiled"

.PHONY:clean
clean:
	@find ${DIR_OBJ} -name *.o -exec rm -rf {} \;