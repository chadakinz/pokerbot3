//
// Created by Chad Gothelf on 6/24/25.
//

#ifndef POKAH_ENVIRONMENT_H
#define POKAH_ENVIRONMENT_H
#include "commonIncludes.h"
int get_potsize(const History& history);
bool is_check(History history);
bool all_in_checker(History history);
int get_next_turn(const History& history);
bool is_terminal(const History& history);
int get_call_amount(const History& history);
Deck get_hand(History history, int i);
std::vector<double> utility(const Config& game_info, const History& history, int i, std::vector<double> dist, std::vector<double> opp_dist);
History process_action(int num, const Config& game_info, const History& history, int i);
Deck get_table_cards(const Config& game_info);
Config river_generator(int max_amount);
int get_potsize(const Config& game_info, const History& history);
std::vector<int> process_hand(Deck hand);
Deck convert_into_deck(std::string str_cards, Deck deck);
bool is_valid_hand(const std::vector<int>& hand);
int get_chips(const Config& game_info, const History& history, int i);
#endif POKAH_ENVIRONMENT_H
