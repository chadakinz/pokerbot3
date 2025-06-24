objects = environment.o attr.o commonIncludes.o
compiler = g++
flags = -g -std=gnu++2b
output = environment
tests = test/test_environment.o environment.o attr.o commonIncludes.o
TEST_BIN = test/test_runner

all: $(output)

$(output): $(objects)
	$(compiler) $(flags) $(objects) -L./lib -lpheval -o ./src/$(output)

test: $(tests)
	$(compiler) $(flags) $(tests) -L./lib -lpheval -o $(TEST_BIN)

%.o: %.cpp
	$(compiler) $(flags) -I./include -c $< -o $@

clean:
	rm -f *.o ./src/$(output)

clean_test:
	rm -f test/test_environment.o