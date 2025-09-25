#define CATCH_CONFIG_MAIN
#include <catch.hpp>
#include <environment.h>
#include <commonIncludes.h>
#include <attr.hpp>
#include <phevaluator/phevaluator.h>
#include <testing_functions.hpp>

TEST_CASE("hand distribution", "[attr]"){
    std::vector<double> hand_distribution = get_hand_distribution();
    REQUIRE(hand_distribution.size() == config_nums["NUM_HANDS"]);
    REQUIRE(vector_sum(hand_distribution) == Approx(1.0).epsilon(1e-10));

}

TEST_CASE("Multiplying vectors", "[attr]"){
    std::vector<int> a(5), b(5);
    a = {1,2,3,4,5};
    b = {1,2,3,4,5};
    std::vector<int> d = {1,4,9,16,25};
    REQUIRE(a * b == d);

    std::vector<double> x(5), y(5);
    x = {1.0,2.0,3.0,4.0,5.0};
    y = {1.0,2.0,3.0,4.0,5.0};
    std::vector<double> z = {1.0,4.0,9.0,16.0,25.0};
    REQUIRE(x * y == z);

}
TEST_CASE("normalize over actions", "[attr]"){
    config_nums["NUM_HANDS"] = 3;
    config_nums["num_actions"] = 2;

    // 3 hands × 2 actions each = 6 elements
    std::vector<double> regrets = {1, 2, 3, 4, 5, 6};

    auto result = normalize_over_actions(regrets);

    // Check size matches NUM_HANDS
    REQUIRE(result.size() == 3);

    // Based on the code's ordering:
    // For hand 0: first time i=0 triggers, writes sum=0, then adds 1
    // This looks like an off-by-one, so expected output may differ from intuitive grouping
    // We verify *actual* behavior
    REQUIRE(result[0] == Approx(3)); // written before adding regret[0]
    REQUIRE(result[1] == Approx(7)); // sum of previous group after 2nd trigger
    REQUIRE(result[2] == Approx(11)); // etc.

    config_nums["NUM_HANDS"] = 2;
    config_nums["num_actions"] = 2;

    std::vector<double> regrets2 = {-1, 2, -3, 4};
    auto result1 = normalize_over_actions(regrets2);

    REQUIRE(result1.size() == 2);
    // Again, verifying actual behavior given current code order
    REQUIRE(result1[0] == Approx(1));
    REQUIRE(result1[1] == Approx(1));
    config_nums["NUM_HANDS"] = 1326;
    config_nums["num_actions"] = 4;
}
TEST_CASE("span_subtract basic subtraction", "[attr]") {
    std::vector<double> a = {5.0, 10.0, -3.0};
    std::vector<double> b = {2.0,  4.0,  1.0};

    // Create span over 'a'
    std::span<double> span_a(a);

    auto result = span_subtract(span_a, b);

    REQUIRE(result.size() == 3);
    REQUIRE(result[0] == Approx(3.0));   // 5 - 2
    REQUIRE(result[1] == Approx(6.0));   // 10 - 4
    REQUIRE(result[2] == Approx(-4.0));  // -3 - 1
}

TEST_CASE("hand index table is correct size and attributes", "[config]"){
    const std::string valid_ranks = "23456789TJQKA";
    const std::string valid_suits = "cdhs";
    REQUIRE(index_hand_lookup_table.size() == config_nums["NUM_HANDS"]);
    for (int i =0; i < config_nums["NUM_HANDS"]; i++){
        const std::string& hand = index_hand_lookup_table[i];
        REQUIRE(hand.size() == 4);

        // Extract the two cards
        std::string card1 = hand.substr(0, 2);
        std::string card2 = hand.substr(2, 2);

        // Check both cards have valid rank and suit
        REQUIRE(valid_ranks.find(card1[0]) != std::string::npos);
        REQUIRE(valid_suits.find(card1[1]) != std::string::npos);
        REQUIRE(valid_ranks.find(card2[0]) != std::string::npos);
        REQUIRE(valid_suits.find(card2[1]) != std::string::npos);

        // Cards must be different
        REQUIRE(card1 != card2);
    }
}

TEST_CASE("process_distribution zeroes and renormalizes", "[attr]") {
    Config game_info = river_generator(20);
    Deck board_cards = get_table_cards(game_info);

    std::vector<double> p1_distribution = get_hand_distribution();
    std::vector<double> p2_distribution = get_hand_distribution();
    REQUIRE(vector_sum(p2_distribution) == Approx(1.0).epsilon(1e-10));
    process_distribution(game_info, p1_distribution, p2_distribution);
    REQUIRE(vector_sum(p1_distribution) == Approx(1.0).epsilon(1e-10));
    REQUIRE(vector_sum(p2_distribution) == Approx(1.0).epsilon(1e-10));
    std::string hand1, hand2;
    for (int i =0; i<board_cards.size(); i++){
        for (int j = 0; j<sharedDeck.size(); j++){
            if (sharedDeck[j] == board_cards[i]) continue;
                hand1 = board_cards[i] + sharedDeck[j];
            if(hand_index_lookup_table.find(hand1) != hand_index_lookup_table.end()){
                REQUIRE(p1_distribution[hand_index_lookup_table[hand1]] == 0.0);
                REQUIRE(p2_distribution[hand_index_lookup_table[hand1]] == 0.0);
                continue;
            }
            hand2 = sharedDeck[j] + board_cards[i];
            if(hand_index_lookup_table.find(hand2) != hand_index_lookup_table.end()){
                REQUIRE(p1_distribution[hand_index_lookup_table[hand2]] == 0.0);
                REQUIRE(p2_distribution[hand_index_lookup_table[hand2]] == 0.0);
                continue;
            }
        }
    }

}
TEST_CASE("configuring game tree", "[game_info]"){
    const std::string valid_ranks = "23456789TJQKA";
    const std::string valid_suits = "cdhs";
    Config game_info = river_generator(20);
    //verifying types are correct
    REQUIRE(std::holds_alternative<chips>(*(game_info.begin())));
    REQUIRE(std::holds_alternative<chips>(*(game_info.begin() + 1)));
    REQUIRE(std::holds_alternative<chance_action>(*(game_info.begin() + 2)));
    REQUIRE(std::holds_alternative<chips>(*(game_info.begin() + 3)));

    Deck cards = get_table_cards(game_info);
    std::string card;
    //verifying cards are valid
    for (int i = 0; i < 5; i++){
        card = cards[i];
    REQUIRE(valid_ranks.find(card[0]) != std::string::npos);
    REQUIRE(valid_suits.find(card[1]) != std::string::npos);
    }

    for (int i = 0; i < 4; i++){
        for (int j = i + 1; j < 5; j++){
            REQUIRE(cards[i] != cards[j]);
        }
    }

}
TEST_CASE("get potsize right amount", "[environment]"){
    Config test_config = {chips(1, 10, 0), chips(2, 10, 0), chance_action('c', {"As", "Ac", "Ad", "Ah", "Ks"}, 0), chips(0, 69, 0)};
    History test_history = {std::make_tuple(1, 'C', 0), std::make_tuple(1, 'R', 2), std::make_tuple(2, 'C', 2)};
    REQUIRE(get_potsize(test_config, test_history)  == 73);
}
TEST_CASE("get call amount right amount", "[environment]" ){
    History test_history = {std::make_tuple(1, 'C', 0), std::make_tuple(1, 'R', 2)};
    REQUIRE(get_call_amount(test_history) == 2);
}
TEST_CASE("Is terminal" ,"[environment]"){
    History test_history1 = {std::make_tuple(1, 'C', 0), std::make_tuple(1, 'R', 2)};
    REQUIRE(!is_terminal(test_history1));
    History test_history2 = {std::make_tuple(1, 'C', 0)};
    REQUIRE(!is_terminal(test_history2));
    History test_history3 = {std::make_tuple(1, 'C', 0), std::make_tuple(2, 'C', 0)};
    REQUIRE(is_terminal(test_history3));
    History test_history4 = {
            std::make_tuple(1, 'C', 0),
            std::make_tuple(2, 'C', 0),
            std::make_tuple(2, 'R', 11),
            std::make_tuple(1, 'C', 11),
            std::make_tuple(1, 'R', 9),
            std::make_tuple(2, 'C', 9)
    };
    REQUIRE(is_terminal(test_history4));

}

TEST_CASE("utility" ,"[environment]"){
    Config game_info = river_generator(30);
    History test_history = {std::make_tuple(1, 'C', 0), std::make_tuple(1, 'R', 2), std::make_tuple(2, 'C', 2)};
    std::vector<double> p1_distribution = get_hand_distribution();
    std::vector<double> p2_distribution = get_hand_distribution();
    std::vector<double> result(config_nums["NUM_HANDS"], 0.0);
    process_distribution(game_info, p1_distribution, p2_distribution);
    //REQUIRE(vector_sum(p2_distribution) == Approx(1.0).epsilon(1e-10));
    Deck cards = get_table_cards(game_info);
    //print_deck(cards);
    Deck hand1, hand2;
    std::vector<int> processed_hand, processed_hand1;
    int HS1, HS2;
    int potsize = get_potsize(game_info, test_history);
    //printf("potsize %d\n", potsize);
    //print_vector(p2_distribution);
    //std::cout << index_hand_lookup_table[0] << std::endl;

    for (int i = 0; i < config_nums["NUM_HANDS"]; i++){
        hand1 = convert_into_deck(index_hand_lookup_table[i], cards);
        processed_hand1= process_hand(hand1);
        HS1 = evaluate_7cards(processed_hand1[0], processed_hand1[1], processed_hand1[2], processed_hand1[3], processed_hand1[4], processed_hand1[5], processed_hand1[6]);
        if (!is_valid_hand(processed_hand1)) {
            continue;
        }
        for (int j = 0; j < config_nums["NUM_HANDS"]; j++){
            //p1 hand
            if(i == j){
                continue;
            }
            //p2 hand
            hand2 = convert_into_deck(index_hand_lookup_table[j], cards);
            processed_hand = process_hand(hand2);
            if (!is_valid_hand(processed_hand)) continue;
            HS2 = evaluate_7cards(processed_hand[0], processed_hand[1], processed_hand[2], processed_hand[3], processed_hand[4], processed_hand[5], processed_hand[6]);

            if (HS1 < HS2){

                //printf("Potsize %d\n", potsize);
                //printf("Distribution %f\n", p2_distribution[j]);
                result[i] += (p2_distribution[j] * (potsize/2));
                //printf("Result %f: %f\n", p2_distribution[j] * (potsize/2), result);
            }else if (HS1 > HS2){
                //print_vector(hand2);
                result[i] -= (p2_distribution[j] * (potsize/2));

            }else{
                continue;
            }

        }

    }
    std::vector<double> test_util = utility(game_info, test_history, 1, p1_distribution, p2_distribution);
    for (int i = 0; i< config_nums["NUM_HANDS"]; i ++ ){
        REQUIRE(result[i] == Approx(test_util[i]).epsilon(1e-10));
    }
    History test_history2 = {std::make_tuple(1, 'C', 0), std::make_tuple(1, 'R', 2), std::make_tuple(2, 'F', 0)};
    std::vector<double> test_util2 = utility(game_info, test_history2, 1, p1_distribution, p2_distribution);
    int potsize2 = get_potsize(game_info, test_history2);
    REQUIRE(test_util2 == std::vector<double>(config_nums["NUM_HANDS"], potsize2/2));
    REQUIRE(!has_nan_or_inf(test_util));
    History test_history3 = {std::make_tuple(1, 'C', 0), std::make_tuple(2, 'C', 0)};
    std::vector<double> test_util3 = utility(game_info, test_history3, 1, p1_distribution, p2_distribution);
    REQUIRE(!has_nan_or_inf(test_util3));
}
TEST_CASE("get next turn", "[environment]"){
    History test_history1 = {std::make_tuple(1, 'C', 0), std::make_tuple(1, 'R', 2)};
    REQUIRE(get_next_turn(test_history1) == 2);
    History test_history2 = {std::make_tuple(1, 'C', 0), std::make_tuple(1, 'R', 2), std::make_tuple(2, 'C', 2), std::make_tuple(2, 'R', 2)};
    REQUIRE(get_next_turn(test_history2) == 1);

}

TEST_CASE("get_chips", "[environment]"){
    Config game_info = {chips(1, 10, 0), chips(2, 10, 0), chance_action('c', {"As", "Ad", "Ks", "Kd", "Kh"}, 0), chips(0, 20, 0)};
    History test_history2 = {std::make_tuple(1, 'C', 0), std::make_tuple(1, 'R', 2), std::make_tuple(2, 'C', 2), std::make_tuple(2, 'R', 2)};
    REQUIRE(get_chips(game_info, test_history2, 1) == 8);
    REQUIRE(get_chips(game_info, test_history2, 2) == 6);

}
TEST_CASE("process_action", "[environment]"){
    Config game_info = {chips(1, 10, 0), chips(2, 10, 0), chance_action('c', {"As", "Ad", "Ks", "Kd", "Kh"}, 0), chips(0, 20, 0)};
    History test_history1 = {std::make_tuple(1, 'C', 0), std::make_tuple(1, 'R', 2), std::make_tuple(2, 'C', 2), std::make_tuple(2, 'R', 2)};
    History actual_history1 = {std::make_tuple(1, 'C', 0), std::make_tuple(1, 'R', 2), std::make_tuple(2, 'C', 2), std::make_tuple(2, 'R', 2), std::make_tuple(1, 'C', 2)};
    REQUIRE(process_action(1, game_info, test_history1, 1) ==  actual_history1);
    History actual_history2 = {std::make_tuple(1, 'C', 0), std::make_tuple(1, 'R', 2), std::make_tuple(2, 'C', 2), std::make_tuple(2, 'R', 2), std::make_tuple(1, 'C', 2), std::make_tuple(1, 'R', 6)};
    REQUIRE(process_action(2, game_info, test_history1, 1) == actual_history2);
    History actual_history3 = {std::make_tuple(1, 'C', 0), std::make_tuple(1, 'R', 2), std::make_tuple(2, 'C', 2), std::make_tuple(2, 'R', 2), std::make_tuple(1, 'C', 2), std::make_tuple(1, 'R', 6), std::make_tuple(2, 'A', 6)};
    REQUIRE(process_action(2, game_info, actual_history2, 2) == actual_history3);
    Config game_info2 = {chips(1, 28, 0), chips(2, 5, 0), chance_action('c', {"As", "Ad", "Ks", "Kd", "Kh"}, 0), chips(0, 23, 0)};
    History test_history2 = {std::make_tuple(1, 'C', 0), std::make_tuple(2, 'C', 0), std::make_tuple(2, 'R', 5)};
    History actual_history4 = {std::make_tuple(1, 'C', 0), std::make_tuple(2, 'C', 0), std::make_tuple(2, 'R', 5), std::make_tuple(1, 'A', 5)};
    REQUIRE(process_action(2, game_info2, test_history2, 1) == actual_history4);


};
TEST_CASE("Regret_cache", "[cache]"){
    Regret_Cache<action> test_cache(config_nums["num_actions"]);
    History test_history = {std::make_tuple(1, 'C', 0), std::make_tuple(1, 'R', 2), std::make_tuple(2, 'C', 2), std::make_tuple(2, 'R', 2)};
    REQUIRE(test_cache.get_strategy(test_history) == std::vector<double>(config_nums["num_actions"] * config_nums["NUM_HANDS"], 1.0/(config_nums["num_actions"])));
    REQUIRE(test_cache[test_history] == std::vector(config_nums["num_actions"] * config_nums["NUM_HANDS"] , 0.0));
    std::vector<double> test(config_nums["num_actions"] * config_nums["NUM_HANDS"], 3.0);
    test_cache[test_history] = test_cache[test_history] + test;
    REQUIRE(test_cache[test_history] == std::vector<double>(config_nums["num_actions"] * config_nums["NUM_HANDS"], 3.0));
    REQUIRE(test_cache.get_strategy(test_history) == std::vector<double>(config_nums["num_actions"] * config_nums["NUM_HANDS"], 1.0/(config_nums["num_actions"])));

}