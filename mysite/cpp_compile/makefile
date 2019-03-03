DIR_INC = ./include
DIR_SRC = ./src
DIR_OBJ = ./obj
DIR_BIN = ./bin

SRC = $(wildcard ${DIR_SRC}/*.cpp)  
OBJ = $(patsubst %.cpp,${DIR_OBJ}/%.o,$(notdir ${SRC})) 

TARGET = test

BIN_TARGET = ${DIR_BIN}/${TARGET}

CC = clang++
CFLAGS = -g -Wall -I${DIR_INC}

${BIN_TARGET}:${OBJ}
	@echo "start to link ${OBJ}"
	$(CC) $(OBJ) -o $@
	@echo "${OBJ} linked"
    
${DIR_OBJ}/%.o:${DIR_SRC}/%.cpp
	@echo "start to compile $*.cpp"
	$(CC) $(CFLAGS) -c $< -o $@
	@echo "$*.cpp compiled"

.PHONY:clean
clean:
	find ${DIR_OBJ} -name *.o -exec rm -rf {} \;