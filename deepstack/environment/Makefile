objects = environment.o attr.o commonIncludes.o testing_functions.o ../CFR.o
compiler = g++
flags = -g -std=gnu++2b
output = CFR
tests = test/test_attr.o environment.o attr.o commonIncludes.o testing_functions.o
TEST_BIN = test/test_runner

all: $(output)

$(output): $(objects)
	$(compiler) $(flags) $(objects) -L./lib -lpheval -o ./src/$(output)

test: $(tests)
	$(compiler) $(flags) $(tests) -v -L./lib -lpheval -o $(TEST_BIN)

%.o: %.cpp
	$(compiler) $(flags) -I./include -c $< -o $@

clean:
	rm -f *.o ../*.o ./src/$(output)

clean_test: clean
	rm -f test/*.o test/test_runner