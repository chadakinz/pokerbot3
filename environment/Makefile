objects = environment.o attr.o commonIncludes.o
compiler = g++
flags = -g -std=gnu++2b
output = environment

all: $(output)

$(output): $(objects)
	$(compiler) $(flags) $(objects) -L./lib -lpheval -o ./src/$(output)

%.o: %.cpp
	$(compiler) $(flags) -I./include -c $< -o $@

clean:
	rm -f *.o ./src/$(output)