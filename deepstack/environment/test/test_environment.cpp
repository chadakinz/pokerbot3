#define CATCH_CONFIG_MAIN
#include <catch.hpp>
#include <environment.h>
#include <commonIncludes.h>

TEST_CASE("Addition works", "[math]") {
    REQUIRE(add(2, 2) == 4);
    REQUIRE(add(-1, 1) == 0);
}
