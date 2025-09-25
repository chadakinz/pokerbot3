#include <commonIncludes.h>

std::random_device rd;
std::mt19937 gen(rd());

const std::vector<std::pair<std::string, int>> hand_rankings = {
        {"AAo", 1},   {"KKo", 2},   {"QQo", 3},   {"AKs", 4},   {"JJo", 5},
        {"AQs", 6},   {"KQs", 7},   {"AJs", 8},   {"KJs", 9},   {"TTo", 10},
        {"AKo", 11},  {"ATs", 12},  {"QJs", 13},  {"KTs", 14},  {"QTs", 15},
        {"JTs", 16},  {"99o", 17},  {"AQo", 18},  {"A9s", 19},  {"KQo", 20},
        {"88o", 21},  {"K9s", 22},  {"T9s", 23},  {"A8s", 24},  {"Q9s", 25},
        {"J9s", 26},  {"AJo", 27},  {"A5s", 28},  {"77o", 29},  {"A7s", 30},
        {"KJo", 31},  {"A4s", 32},  {"A3s", 33},  {"A6s", 34},  {"QJo", 35},
        {"66o", 36},  {"K8s", 37},  {"T8s", 38},  {"A2s", 39},  {"98s", 40},
        {"J8s", 41},  {"ATo", 42},  {"Q8s", 43},  {"K7s", 44},  {"KTo", 45},
        {"55o", 46},  {"JTo", 47},  {"87s", 48},  {"QTo", 49},  {"44o", 50},
        {"33o", 51},  {"22o", 52},  {"K6s", 53},  {"97s", 54},  {"K5s", 55},
        {"76s", 56},  {"T7s", 57},  {"K4s", 58},  {"K3s", 59},  {"K2s", 60},
        {"Q7s", 61},  {"86s", 62},  {"65s", 63},  {"J7s", 64},  {"54s", 65},
        {"Q6s", 66},  {"75s", 67},  {"96s", 68},  {"Q5s", 69},  {"64s", 70},
        {"Q4s", 71},  {"Q3s", 72},  {"T9o", 73},  {"T6s", 74},  {"Q2s", 75},
        {"A9o", 76},  {"53s", 77},  {"85s", 78},  {"J6s", 79},  {"J9o", 80},
        {"K9o", 81},  {"J5s", 82},  {"Q9o", 83},  {"43s", 84},  {"74s", 85},
        {"J4s", 86},  {"J3s", 87},  {"95s", 88},  {"J2s", 89},  {"63s", 90},
        {"A8o", 91},  {"52s", 92},  {"T5s", 93},  {"84s", 94},  {"T4s", 95},
        {"T3s", 96},  {"42s", 97},  {"T2s", 98},  {"98o", 99},  {"T8o", 100},
        {"A5o", 101}, {"A7o", 102}, {"73s", 103}, {"A4o", 104}, {"32s", 105},
        {"94s", 106}, {"93s", 107}, {"J8o", 108}, {"A3o", 109}, {"62s", 110},
        {"92s", 111}, {"K8o", 112}, {"A6o", 113}, {"87o", 114}, {"Q8o", 115},
        {"83s", 116}, {"A2o", 117}, {"82s", 118}, {"97o", 119}, {"72s", 120},
        {"76o", 121}, {"K7o", 122}, {"65o", 123}, {"T7o", 124}, {"K6o", 125},
        {"86o", 126}, {"54o", 127}, {"K5o", 128}, {"J7o", 129}, {"75o", 130},
        {"Q7o", 131}, {"K4o", 132}, {"K3o", 133}, {"96o", 134}, {"K2o", 135},
        {"64o", 136}, {"Q6o", 137}, {"53o", 138}, {"85o", 139}, {"T6o", 140},
        {"Q5o", 141}, {"43o", 142}, {"Q4o", 143}, {"Q3o", 144}, {"74o", 145},
        {"Q2o", 146}, {"J6o", 147}, {"63o", 148}, {"J5o", 149}, {"95o", 150},
        {"52o", 151}, {"J4o", 152}, {"J3o", 153}, {"42o", 154}, {"J2o", 155},
        {"84o", 156}, {"T5o", 157}, {"T4o", 158}, {"32o", 159}, {"T3o", 160},
        {"73o", 161}, {"T2o", 162}, {"62o", 163}, {"94o", 164}, {"93o", 165},
        {"92o", 166}, {"83o", 167}, {"82o", 168}, {"72o", 169}
};

Deck initializeSharedDeck() {
    Deck deck;
    std::vector<std::string> ranks = {"2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"};
    std::vector<std::string> suits = {"s", "d", "c", "h"};
    for (const auto& suit : suits) {
        for (const auto& rank : ranks) {
            deck.emplace_back(rank + suit);
        }
    }
    return deck;
}
std::vector<std::string> initialize_hand_table(){
    std::vector<char> suits = {'s', 'd', 'c', 'h'};
    std::vector<std::string> hand_table;
    std::string card1;
    std::string card2;
    for (const auto& [hand, rank]: hand_rankings){

        if(hand[2] == 'o'){
            if(hand[0] == hand[1]){
                for (int i = 0; i < suits.size(); i++) {
                    card1 = "";
                    card1 += hand[0];
                    card1 += suits[i];
                    for (int j = i; j < suits.size(); j++) {
                        card2 = "";
                        if (suits[i] == suits[j]) {
                            continue;
                        }
                        card2 += hand[1];
                        card2 += suits[j];
                        hand_table.push_back(card1 + card2);
                    }
                }
            }else{
                for (int i = 0; i < suits.size(); i++) {
                    card1 = "";
                    card1 += hand[0];
                    card1 += suits[i];
                    for (int j = i; j < suits.size(); j++) {
                        card2 = "";
                        if (suits[i] == suits[j]) {
                            continue;
                        }
                        card2 += hand[1];
                        card2 += suits[j];
                        hand_table.push_back(card1 + card2);
                    }
                }
                for (int i = 0; i < suits.size(); i++) {
                    card1 = "";
                    card1 += hand[1];
                    card1 += suits[i];
                    for (int j = i; j < suits.size(); j++) {
                        card2 = "";
                        if (suits[i] == suits[j]) {
                            continue;
                        }
                        card2 += hand[0];
                        card2 += suits[j];
                        hand_table.push_back(card1 + card2);
                    }
                }
            }
        }
        else{
            for (int i = 0; i < suits.size(); i++){
                card1 = "";
                card2 = "";
                card1 += hand[0];
                card1 += suits[i];
                card2 += hand[1];
                card2 += suits[i];
                hand_table.push_back(card1 + card2);
            }
        }
    }
    return hand_table;
}
std::vector<std::string> index_hand_lookup_table = initialize_hand_table();

std::unordered_map<std::string, int> initialize_hand_index_lookup_table(){
    std::unordered_map<std::string, int> hand_index_lookup_table;
    for (int i = 0; i< index_hand_lookup_table.size(); i++){
        hand_index_lookup_table[index_hand_lookup_table[i]] = i;
    }
    return hand_index_lookup_table;
}



std::unordered_map<std::string, int> hand_index_lookup_table = initialize_hand_index_lookup_table();
Deck sharedDeck = initializeSharedDeck();

std::unordered_map<std::string, int> config_nums = {{"NUM_HANDS", 1326}, {"num_actions", 4}, {"num_samples", 1},
                                                    {"max_chip_amount", 50}, {"cfr_iterations", 5000}, {"deck_size", 52},
                                                    {"num_ranks", 13}, {"num_suits", 4}};


std::unordered_map<std::string, int> initialize_deck_lookup_table(){
    std::unordered_map<std::string, int> deck_lookup_table;
    for (int i = 0; i < sharedDeck.size(); i++){
        deck_lookup_table[sharedDeck[i]] = i;
    }
    return deck_lookup_table;
}
std::unordered_map<char, int> initialize_rank_lookup_table(){
    std::vector<char> ranks = {'2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A'};
    std::unordered_map<char, int> rank_lookup_table;
    for (int i = 0; i < ranks.size(); i++){
        rank_lookup_table[ranks[i]] = i;
    }
    return rank_lookup_table;
}

std::unordered_map<char, int> initialize_suit_lookup_table(){
    std::vector<char> suits = {'s', 'd', 'c', 'h'};
    std::unordered_map<char, int> suit_lookup_table;
    for(int i = 0; i< suits.size(); i++){
        suit_lookup_table[suits[i]] = i;
    }
    return suit_lookup_table;
}
std::unordered_map<std::string, int> deck_lookup_table = initialize_deck_lookup_table();
std::unordered_map<char, int> rank_lookup_table = initialize_rank_lookup_table();
std::unordered_map<char, int> suit_lookup_table = initialize_suit_lookup_table();