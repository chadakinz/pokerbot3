#include <commonIncludes.h>
#include <attr.hpp>
#include <environment.h>
#include <span>
#include <utility>

std::vector<double> span_subtract(std::span<double> s, std::vector<double> v){
    std::vector<double> v2(v.size());
    for (int i =0; i < v.size(); i++){
        v2[i] = s[i] - v[i];
    }
    return v2;
}
//todo ineffecniet, dont need to configurate vector size, can just emplace back or reference result from another function
std::vector<double> update_distribution(const std::vector<double>& dist, const std::span<double>& strategy_a_I){
    std::vector<double> updated_distribution(config_nums["NUM_HANDS"]);
    for (int i = 0; i < config_nums["NUM_HANDS"]; i++){
        updated_distribution[i] = dist[i] * strategy_a_I[i];
    }
    double sum = vector_sum(updated_distribution);

    for (int i = 0; i < config_nums["NUM_HANDS"]; i++){
        updated_distribution[i] /= sum;
    }
    return updated_distribution;
}
bool elem(const std::string& needle, const std::string& haystack){
    return haystack.find(needle) != std::string::npos;
}


void process_distribution(const Config& game_info, std::vector<double>& p1_distribution, std::vector<double>& p2_distribution){
    std::string hand1, hand2;
    Deck board_cards = get_table_cards(game_info);
    for (int i =0; i<board_cards.size(); i++){
         for (int j = 0; j<sharedDeck.size(); j++){
             if (sharedDeck[j] == board_cards[i]) continue;
             hand1 = board_cards[i] + sharedDeck[j];
             if(hand_index_lookup_table.find(hand1) != hand_index_lookup_table.end()){
                 p1_distribution[hand_index_lookup_table[hand1]] = 0.0;
                 p2_distribution[hand_index_lookup_table[hand1]] = 0.0;
                 continue;
             }
             hand2 = sharedDeck[j] + board_cards[i];
             if(hand_index_lookup_table.find(hand2) != hand_index_lookup_table.end()){
                 p1_distribution[hand_index_lookup_table[hand2]] = 0.0;
                 p2_distribution[hand_index_lookup_table[hand2]] = 0.0;
                 continue;
             }
         }
    }
    double sum1 = vector_sum(p1_distribution);
    double sum2 = vector_sum(p2_distribution);
    for (int k = 0; k<config_nums["NUM_HANDS"]; k ++){
        p1_distribution[k] /= sum1;
        p2_distribution[k] /= sum2;
    }
}

void generate_hand_distribution(std::vector<double>& hand_distribution, double p, int start, int end){
    std::uniform_real_distribution<double> dist(0.0, p);
    // Generate a number
    if (end - start == 0){
        return;
    }else if( end - start == 1){
        hand_distribution[start] = p;
    }else{
        double p1 = dist(gen);
        double p2 = p - p1;
        int half = (end + start)/2;
        generate_hand_distribution(hand_distribution, p1, start, half);
        generate_hand_distribution(hand_distribution, p2, half, end);
    }

}
std::vector<double> normalize_over_actions(const std::vector<double>& regret_matrix) {
    double sum = 0.0;
    int count = 0;
    std::vector<double> normalized_matrix(config_nums["NUM_HANDS"]);
    for (int i = 1; i < regret_matrix.size() + 1; i++){
        sum += regret_matrix[i - 1];
        if (i % config_nums["num_actions"] == 0){
            normalized_matrix[count] = sum;
            sum = 0;
            count ++;
        }
    }
    return normalized_matrix;
}
std::vector<double> get_hand_distribution(){
    std::vector<double> hand_distribution = std::vector(config_nums["NUM_HANDS"], 0.0);
    generate_hand_distribution(hand_distribution, 1, 0, config_nums["NUM_HANDS"]);
    return hand_distribution;
}

Deck chance_sample(int num_cards, const Deck& deck){
    int n = deck.size();
    std::uniform_int_distribution<> dist(0,  n - 1);
    int sampled_num;
    Deck cards(num_cards);
    for (int i = 0; i < num_cards; i++){
        sampled_num = dist(gen);
        cards[i] = sharedDeck[sampled_num];
        std::swap(sharedDeck[sampled_num], sharedDeck[n - 1]);
        n --;
        dist = std::uniform_int_distribution<>(0, n - 1);
    }

    return cards;
}



//TODO, can shorten the runtime of this function
/*
std::vector<double> get_infoset(const History& history){
    std::vector<double> infoset;
    std::vector<double> deck_card_encode(config_nums["deck_size"], 0.0);
    std::vector<double> rank_encode(config_nums["num_ranks"], 0.0);
    std::vector<double> suit_encode(config_nums["num_suits"], 0.0);
    double effective_stack = std::max(1.0, std::min(get_chips(history, 1), get_chips(history,2)));
    double potsize = effective_stack/(double) get_potsize(history); //Using SPR instead of pot/player stacks
    Deck board = get_table_cards(history);
    int deck_card_index, rank_index, suit_index;


    for (std::string& card: board){
        deck_card_index = deck_lookup_table[card];
        deck_card_encode[deck_card_index] = 1.0;

        rank_index = rank_lookup_table[card[0]];
        rank_encode[rank_index] += 1.0;

        suit_index = suit_lookup_table[card[1]];
        suit_encode[suit_index] += 1.0;

    }
    infoset.emplace_back(potsize);
    infoset.insert(infoset.end(), deck_card_encode.begin(), deck_card_encode.end());
    infoset.insert(infoset.end(), rank_encode.begin(), rank_encode.end());
    infoset.insert(infoset.end(), suit_encode.begin(), suit_encode.end());


    return infoset;
}
 */