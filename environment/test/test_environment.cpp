#define CATCH_CONFIG_MAIN
#include <catch.hpp>
#include <environment.h>
#include <commonIncludes.h>
int add(int a, int b) {
    return a + b;
}

TEST_CASE("Addition works", "[math]") {
    REQUIRE(add(2, 2) == 4);
    REQUIRE(add(-1, 1) == 0);
}
TEST_CASE("getting potsize", "[environment]"){
    History history1 = { player_chips(1, 40, 0),
                        player_chips(2, 25, 0),
                        chance_action('c', {"Jh", "Jc"}, 0),
                        chance_action('c', {"Qs", "Qc"}, 0),
                        player_action(2, 'R', 1),
                        player_action(1, 'C', 1),
                        player_action(1, 'R', 1),
                        player_action(2, 'C', 1),
                        chance_action('c', {"Ad", "Kh", "Ks"}, 0),
                        player_action(1, 'C', 0),
                        player_action(1, 'R', 4),
                        player_action(2, 'C', 4),
                        chance_action('c', {"As"}, 0),
                        player_action(1, 'C', 0),
                        player_action(1, 'R', 6)};
    REQUIRE(get_potsize(history1) == 18);
}

TEST_CASE("is check", "[environment]"){
    History history1 = { player_chips(1, 40, 0),
                         player_chips(2, 25, 0),
                         chance_action('c', {"Jh", "Jc"}, 0),
                         chance_action('c', {"Qs", "Qc"}, 0),
                         player_action(2, 'R', 1),
                         player_action(1, 'C', 1),
                         player_action(1, 'R', 1),
                         player_action(2, 'C', 1),
                         chance_action('c', {"Ad", "Kh", "Ks"}, 0),
                         player_action(1, 'C', 0),
                         player_action(1, 'R', 4),
                         player_action(2, 'C', 4),
                         chance_action('c', {"As"}, 0),
                         player_action(1, 'C', 0)};
    REQUIRE(is_check(history1) == false);

}

TEST_CASE("all in checker", "[environment]"){
    History history1 = { player_chips(1, 40, 0),
                         player_chips(2, 25, 0),
                         chance_action('c', {"Jh", "Jc"}, 0),
                         chance_action('c', {"Qs", "Qc"}, 0),
                         player_action(2, 'R', 1),
                         player_action(1, 'C', 1),
                         player_action(1, 'R', 1),
                         player_action(2, 'C', 1),
                         chance_action('c', {"Ad", "Kh", "Ks"}, 0),
                         player_action(1, 'C', 0),
                         player_action(1, 'R', 4),
                         player_action(2, 'C', 4),
                         chance_action('c', {"As"}, 0),
                         player_action(1, 'C', 0)};
History history2 = { player_chips(1, 40, 0),
                     player_chips(2, 25, 0),
                     chance_action('c', {"Jh", "Jc"}, 0),
                     chance_action('c', {"Qs", "Qc"}, 0),
                     player_action(2, 'R', 1),
                     player_action(1, 'C', 1),
                     player_action(1, 'R', 1),
                     player_action(2, 'C', 1),
                     chance_action('c', {"Ad", "Kh", "Ks"}, 0),
                     player_action(1, 'C', 0),
                     player_action(1, 'R', 4),
                     player_action(2, 'C', 4),
                     chance_action('c', {"As"}, 0),
                     player_action(1, 'R', 16),
                     player_action(1, 'A', 16)};
    REQUIRE(all_in_checker(history2) == true);
    History history3 = { player_chips(1, 40, 0),
                         player_chips(2, 25, 0),
                         chance_action('c', {"Jh", "Jc"}, 0),
                         chance_action('c', {"Qs", "Qc"}, 0),
                         player_action(2, 'R', 1),
                         player_action(1, 'C', 1),
                         player_action(1, 'R', 1),
                         player_action(2, 'C', 1),
                         player_action(2, 'R', 23),
                         player_action(1, 'A', 23),
                         chance_action('c', {"Ad", "Kh", "Ks"}, 0),
                         chance_action('c', {"As"}, 0)};
    REQUIRE(all_in_checker(history3) == true);

}
TEST_CASE("get next turn", "[environment]"){
    History history1 = { player_chips(1, 40, 0),
                         player_chips(2, 25, 0),
                         chance_action('c', {"Jh", "Jc"}, 0),
                         chance_action('c', {"Qs", "Qc"}, 0),
                         player_action(2, 'R', 1),
                         player_action(1, 'C', 1),
                         player_action(1, 'R', 1),
                         player_action(2, 'C', 1),
                         chance_action('c', {"Ad", "Kh", "Ks"}, 0),
                         player_action(1, 'C', 0),
                         player_action(1, 'R', 4),
                         player_action(2, 'C', 4),
                         chance_action('c', {"As"}, 0),
                         player_action(1, 'C', 0)};
    REQUIRE(get_next_turn(history1) == 2);
    History history2 = { player_chips(1, 40, 0),
                         player_chips(2, 25, 0),
                         chance_action('c', {"Jh", "Jc"}, 0),
                         chance_action('c', {"Qs", "Qc"}, 0),
                         player_action(2, 'R', 1),
                         player_action(1, 'C', 1),
                         player_action(1, 'R', 1),
                         player_action(2, 'C', 1),
                         chance_action('c', {"Ad", "Kh", "Ks"}, 0),
                         player_action(1, 'C', 0),
                         player_action(1, 'R', 4),
                         player_action(2, 'C', 4),
                         chance_action('c', {"As"}, 0)};
    REQUIRE(get_next_turn(history2) == 1);
    History history3 = { player_chips(1, 40, 0),
                         player_chips(2, 25, 0),
                         chance_action('c', {"Jh", "Jc"}, 0),
                         chance_action('c', {"Qs", "Qc"}, 0),
                         player_action(2, 'R', 1),
                         player_action(1, 'C', 1),
                         player_action(1, 'R', 1),
                         player_action(2, 'C', 1),
                         chance_action('c', {"Ad", "Kh", "Ks"}, 0),
                         player_action(1, 'C', 0),
                         player_action(1, 'R', 4),
                         player_action(2, 'C', 4)};
    REQUIRE(get_next_turn(history3) == 'c');
    History history4 = { player_chips(1, 40, 0),
                         player_chips(2, 25, 0),
                         chance_action('c', {"Jh", "Jc"}, 0),
                         chance_action('c', {"Qs", "Qc"}, 0),
                         player_action(2, 'R', 1),
                         player_action(1, 'C', 1),
                         player_action(1, 'R', 1),
                         player_action(2, 'C', 1),
                         chance_action('c', {"Ad", "Kh", "Ks"}, 0),
                         player_action(1, 'C', 0),
                         player_action(1, 'R', 4),
                         player_action(2, 'C', 4),
                         chance_action('c', {"As"}, 0),
                         player_action(1, 'R', 16),
                         player_action(1, 'A', 16)};
    REQUIRE(get_next_turn(history4) == 'c');
    History history5 = { player_chips(1, 40, 0),
                         player_chips(2, 25, 0),
                         chance_action('c', {"Jh", "Jc"}, 0),
                         chance_action('c', {"Qs", "Qc"}, 0),
                         player_action(2, 'R', 1),
                         player_action(1, 'C', 1),
                         player_action(1, 'R', 1),
                         player_action(2, 'C', 1),
                         player_action(2, 'R', 23),
                         player_action(1, 'A', 23),
                         chance_action('c', {"Ad", "Kh", "Ks"}, 0),
                         chance_action('c', {"As"}, 0)};
    REQUIRE(get_next_turn(history5) == 'c');
}
TEST_CASE("is terminal", "[environment]"){
    History history1 = { player_chips(1, 40, 0),
                         player_chips(2, 25, 0),
                         chance_action('c', {"Jh", "Jc"}, 0),
                         chance_action('c', {"Qs", "Qc"}, 0),
                         player_action(2, 'R', 1),
                         player_action(1, 'C', 1),
                         player_action(1, 'R', 1),
                         player_action(2, 'C', 1),
                         chance_action('c', {"Ad", "Kh", "Ks"}, 0),
                         player_action(1, 'C', 0),
                         player_action(1, 'R', 4),
                         player_action(2, 'C', 4),
                         chance_action('c', {"As"}, 0),
                         player_action(1, 'C', 0),
                         player_action(1, 'R', 6)};
    REQUIRE(is_terminal(history1) == false);
    History history2 = { player_chips(1, 40, 0),
                         player_chips(2, 25, 0),
                         chance_action('c', {"Jh", "Jc"}, 0),
                         chance_action('c', {"Qs", "Qc"}, 0),
                         player_action(2, 'R', 1),
                         player_action(1, 'C', 1),
                         player_action(1, 'R', 1),
                         player_action(2, 'C', 1),
                         chance_action('c', {"Ad", "Kh", "Ks"}, 0),
                         player_action(1, 'C', 0),
                         player_action(1, 'R', 4),
                         player_action(2, 'C', 4),
                         chance_action('c', {"As"}, 0),
                         player_action(1, 'C', 0),
                         player_action(1, 'R', 6),
                         player_action(2, 'F', 0)};
    REQUIRE(is_terminal(history2) == true);
}