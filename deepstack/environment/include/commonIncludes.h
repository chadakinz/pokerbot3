#pragma once
#include <stdio.h>
#include <tuple>
#include <vector>
#include <string>
#include <random>
#include <any>
#include <variant>
#include <unordered_map>
#include <map>
#include <iostream>
#include <array>
#include <numeric>
#include <functional>



using Deck = std::vector<std::string>;
using chance_action = std::tuple<char, Deck, int>;
using player_action = std::tuple<int, char, int>;
using chips = std::tuple<int, int, int>;
using action_type = std::variant<chance_action, chips>;
using Config = std::vector<action_type>;
using action =  std::tuple<int, char, int>;
using History = std::vector<action>;

extern std::vector<std::string> index_hand_lookup_table;
extern std::random_device rd;
extern std::mt19937 gen;
extern Deck sharedDeck;

extern std::unordered_map<std::string, int> config_nums;
extern std::unordered_map<std::string, int> deck_lookup_table;
extern std::unordered_map<char, int> rank_lookup_table;
extern std::unordered_map<char, int> suit_lookup_table;

extern std::unordered_map<std::string, int> hand_index_lookup_table;

constexpr int NUM_HANDS = 1326;
constexpr int NUM_ACTIONS = 4;
constexpr int NUM_SAMPLES = 10000;
constexpr int CFR_ITERATIONS = 100;
constexpr int DECK_SIZE = 52;
constexpr int NUM_RANKS = 13;
constexpr int NUM_SUITS = 4;