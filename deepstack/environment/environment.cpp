#include <commonIncludes.h>
#include <attr.hpp>
#include <phevaluator/phevaluator.h>
#include <algorithm>
//std::get<x>(tuple) -->std::get<x>(std::get<player_action>(variant));

//Generates a random river scenario
//todo make sure potsize can only be an even amount
Config river_generator(int max_amount){
    std::uniform_int_distribution<> player_chips_dist(1, max_amount);
    int p1_chips = player_chips_dist(gen);
    int p2_chips = player_chips_dist(gen);
    std::uniform_int_distribution<> pot_chips_dist(2, (max_amount - p1_chips) + (max_amount - p2_chips));
    int psize = pot_chips_dist(gen);
    Deck cards = chance_sample(5, sharedDeck);
    Config game_tree;
    game_tree.emplace_back(chips(1, p1_chips, 0));
    game_tree.emplace_back(chips(2, p2_chips, 0));
    game_tree.emplace_back(chance_action('c', cards, 0));
    game_tree.emplace_back(chips(0, psize, 0));
    return game_tree;
}

int process_card(std::string card){
    char rank = card[0];
    int rank_val;
    char suit = card[1];
    int suit_val;
    if (rank == 'T') rank_val = 8;
    else if (rank == 'J') rank_val = 9;
    else if (rank == 'Q') rank_val = 10;
    else if (rank == 'K') rank_val = 11;
    else if (rank == 'A') rank_val = 12;
    else{
        rank_val = rank - ('0' + 2);
    }
    if (suit == 'c') suit_val = 0;
    else if (suit == 'd') suit_val = 1;
    else if (suit == 'h') suit_val = 2;
    else if (suit == 's') suit_val = 3;

    return rank_val*4 + suit_val;

}
std::vector<int> process_hand(Deck hand){
    std::vector<int> new_hand = {};
    for(auto& card: hand){
        new_hand.emplace_back(process_card(card));
    }
    return new_hand;
}

int get_potsize(const Config& game_info, const History& history){
    int potsize = std::get<1>(std::get<chips>(*(game_info.begin() + 3)));;
    for(auto action = history.begin(); action != history.end(); action++){
        potsize += std::get<2>(*action);
    }
    return potsize;
}

int get_call_amount(const History& history){
    if (history.size() == 0) return 0;
    auto last_action = *history.rbegin();
    return std::get<2>(last_action);
}


int get_chips(const Config& game_info, const History& history, int i){
    int player_chips;
    if (i == 1){
        player_chips = std::get<1>(std::get<chips>(*(game_info.begin())));

    }else{
        player_chips = std::get<1>(std::get<chips>(*(game_info.begin() + 1)));
    }
    for(auto action = history.begin(); action != history.end(); action++){
        if (std::get<0>(*action) == i){
            player_chips -= std::get<2>(*action);
        }
    }
    return player_chips;
}

bool is_check(const History& history){
    int n = history.size();
    if(n > 0){
        return true;
    }else{
        return false;
    }
}

int get_next_turn(const History& history){
    if (history.size() == 0){
        return 1;
    }
    int id = std::get<0>(*history.rbegin());
    if (id == 1) return 2;
    else return 1;
}

bool is_terminal(const History& history) {
    if (history.size() == 0){
        return false;
    }
    auto last_action = *(history.rbegin());
    auto last_val = std::get<1>(last_action);
    if (last_val == 'F') return true;
    else if(last_val == 'A') return true;
    else if (last_val == 'R') return false;
    else if (history.size() > 1 && last_val == 'C') return true;
    else return false;
}

Deck get_table_cards(const Config& game_info){
    return std::get<1>(std::get<chance_action>(*(game_info.begin() + 2)));
}

Deck convert_into_deck(std::string str_cards, Deck deck){
    deck.push_back(str_cards.substr(0, 2));
    deck.push_back(str_cards.substr(2, 2));
    return deck;
}

bool is_valid_hand(const std::vector<int>& hand) {
    if (hand.size() != 7) return false;
    bool seen[52] = {false};

    for (int card : hand) {
        if (card < 0 || card >= 52) return false;
        if (seen[card]) return false;
        seen[card] = true;
    }
    return true;
}
//todo make sure you either round pot or keep it as a decimal
std::vector<double> utility(const Config& game_info, const History& history, int i, std::vector<double> dist, std::vector<double> opp_dist){
    int opp_id;
    if (i == 1) opp_id = 2;
    else opp_id = 1;
    int pot = get_potsize(game_info, history);
    if (std::get<1>(*history.rbegin()) == 'F'){
        if (std::get<0>(*history.rbegin()) == opp_id){
            return std::vector<double>(config_nums["NUM_HANDS"], pot/2);
        }else{
            return std::vector<double>(config_nums["NUM_HANDS"], -pot/2);
        }
    }
    std::vector<double> Utility(config_nums["NUM_HANDS"], 0.0);
    std::vector<std::tuple<int, int>> hand_strength(config_nums["NUM_HANDS"], std::make_tuple(-1, -1));
    double win_percent = 1.0;
    double copy_win_percent = 1.0;
    Deck cards = get_table_cards(game_info);
    Deck hand;
    std::vector<int> processed_hand;

    int current_hand_strength, prev_hand_strength;
    std::unordered_map<int, double> cum_hand_strength;
    int index;
    for(int i = 0; i < config_nums["NUM_HANDS"]; i++){
        hand = convert_into_deck(index_hand_lookup_table[i], cards);
        processed_hand = process_hand(hand);
        if (!is_valid_hand(processed_hand)) {
            hand_strength[i] = std::make_tuple(-1, i);
            continue;
        }
        current_hand_strength = evaluate_7cards(processed_hand[0], processed_hand[1], processed_hand[2], processed_hand[3], processed_hand[4], processed_hand[5], processed_hand[6]);
        hand_strength[i] = std::make_tuple(current_hand_strength, i);
        if(cum_hand_strength.contains(current_hand_strength)){
            cum_hand_strength[current_hand_strength] += opp_dist[i];
        }
        else{
            cum_hand_strength[current_hand_strength] = opp_dist[i];
        }
    }
    std::sort(hand_strength.begin(), hand_strength.end(), [](const auto& a, const auto& b) {
        return std::get<0>(a)<std::get<0>(b);
    });

    for(int hand = 0; hand < config_nums["NUM_HANDS"]; hand ++){
        index = std::get<1>(hand_strength[hand]);
        if (std::get<0>(hand_strength[hand]) == -1){
            Utility[index] = 0;
            continue;
        }

        current_hand_strength = std::get<0>(hand_strength[hand]);
        if(current_hand_strength != prev_hand_strength){
            win_percent -= cum_hand_strength[prev_hand_strength];
        }
        copy_win_percent = win_percent - (cum_hand_strength[current_hand_strength]);
        Utility[index] = ((copy_win_percent * (pot/2) - (1.0 - win_percent) * (pot/2)));
        prev_hand_strength = current_hand_strength;
    }
    //printf("Issue\n\n");
    return Utility;
}

History process_action4(int num, const Config& game_info, History history, int i){
    int opp_id;
    if (i == 1) opp_id = 2;
    else opp_id = 1;
    int call_amount, pot, raise_amount;
    int chips = get_chips(game_info, history, i);
    int opp_chips = get_chips(game_info, history, opp_id);
    //printf("print get chips: %d\n", opp_chips);
    switch (num){
        case 0:
            history.emplace_back(std::make_tuple(i, 'F', 0));
            return history;
        case 1:
            call_amount = get_call_amount(history);
            if (chips <= call_amount) history.emplace_back(std::make_tuple(i, 'A', chips));
            else history.emplace_back(std::make_tuple(i, 'C', call_amount));
            //printf("HELLLLOOO 2\n");
            return history;

        case 2:
            pot = get_potsize(game_info, history);
            call_amount = get_call_amount(history);
            raise_amount = pot;
            if (chips <= call_amount) history.emplace_back(std::make_tuple(i, 'A', chips));
            else if (opp_chips <= 0) history.emplace_back(std::make_tuple(i, 'A', call_amount));
            else if (raise_amount < call_amount){
                history.emplace_back(std::make_tuple(i, 'C', call_amount));
                history.emplace_back(std::make_tuple(i, 'R', std::min({chips - call_amount, opp_chips, call_amount})));
            }
            else{
                history.emplace_back(std::make_tuple(i, 'C', call_amount));
                history.emplace_back(std::make_tuple(i, 'R', std::min({chips - call_amount, opp_chips, raise_amount})));
            }
            //printf("HELLLLOOO 3\n");
            return history;
        case 3:
            call_amount = get_call_amount(history);
            if (chips <= call_amount) history.emplace_back(std::make_tuple(i, 'A', chips));
            else if(opp_chips <= 0) history.emplace_back(std::make_tuple(i, 'A', call_amount));
            else{
                history.emplace_back(std::make_tuple(i, 'C', call_amount));
                history.emplace_back(std::make_tuple(i, 'R', std::min({chips - call_amount, opp_chips})));
                }
            //printf("HELLLLOOO 4\n");
            return history;
     }
}
History process_action5(int num, const Config& game_info, History history, int i){
    return {};
}
History process_action6(int num, const Config& game_info, History history, int i){
    return {};
}
History process_action(int num, const Config& game_info, const History& history, int i) {
    if (config_nums["num_actions"] == 4) return process_action4(num, game_info, history, i);
    else if (config_nums["num_actions"] == 5) return process_action5(num, game_info, history, i);
    else if (config_nums["num_actions"] == 6) return process_action6(num, game_info, history, i);
    else throw std::runtime_error("num actions is not configured");
}