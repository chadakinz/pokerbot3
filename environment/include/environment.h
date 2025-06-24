//
// Created by Chad Gothelf on 6/24/25.
//

#ifndef POKAH_ENVIRONMENT_H
#define POKAH_ENVIRONMENT_H
#include <commonIncludes.h>
int get_potsize(History history);
bool is_check(History history);
bool all_in_checker(History history);
int get_next_turn(History history);
bool is_terminal(History history);
#endif //POKAH_ENVIRONMENT_H
