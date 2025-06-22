objects = environment.o attr.o commonIncludes.o
compiler = g++
flags = -g -std=gnu++2b
output = environment

all: $(output)

$(output): $(objects)
	$(compiler) $(flags) $(objects) -o ./src/$(output)

%.o: %.cpp
	$(compiler) $(flags) -c $< -o $@

clean:
	rm -f *.o ./src/$(output)