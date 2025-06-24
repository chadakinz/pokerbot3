#ifndef COMMONINCLUDES_H
#define COMMONINCLUDES_H

#include <stdio.h>
#include <tuple>
#include <vector>
#include <string>
#include <random>
#include <any>
#include <variant>

using Deck = std::vector<std::string>;
using chance_action = std::tuple<char, Deck, int>;
using player_action = std::tuple<int, char, int>;
using player_chips = std::tuple<int, int, int>;
using action_type = std::variant<chance_action, player_action, player_chips>;
using History = std::vector<action_type>;

extern std::random_device rd;
extern std::mt19937 gen;
extern Deck sharedDeck;

void initializeSharedDeck();
#endif