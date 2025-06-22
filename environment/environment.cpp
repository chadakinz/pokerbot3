#include "commonIncludes.h"
#include "attr.h"


History intialize_tree(int max_amount){
    std::uniform_int_distribution<> dist(1, max_amount);
    int p1_chips = dist(gen);
    int p2_chips = dist(gen);
    Deck cards = chance_sample(4, sharedDeck);
    History game_tree;
    game_tree.emplace_back(player_action(1, p1_chips, 0));
    game_tree.emplace_back(player_action(2, p2_chips, 0));
    game_tree.emplace_back(chance_action('c', Deck(cards.begin(), cards.begin() + 2), 0));
    game_tree.emplace_back(chance_action('c', Deck(cards.begin() + 2, cards.begin() + 4), 0));
    game_tree.emplace_back(player_action(2, 'R', 1));
    game_tree.emplace_back(player_action(1, 'C', 1));
    game_tree.emplace_back(player_action(1, 'R', 1));

    return game_tree;
}
int get_next_turn(History history){
    int n = history.size();

    if (n == 7) return 2;


    else {
        auto last_action = *history.rbegin();
        bool chance_action_b =  std::holds_alternative<chance_action>(last_action);
        bool all_in = all_in_checker(history);
        //street = get_betting_round(history);
        if (all_in) return 'c';
        if (chance_action_b) return 1;
        bool check = false;
        for (auto it = history.rbegin() + 1; it != history.rend(); it ++){
            item = *it;
            if (std::get<0>(item) == 'c') break;
            if ((std::get<1>(item) == 'R') || (std::get<1>(item) == 'C')) {
                check = true;
                break;
            }
        }

        if ((std::get<1>(last_action) == 'C') && check){
            return 'c';
        }else if ((std::get<1>(last_action) == 'C') && !check){
            return 2;
        }

        if count > 1:
        return 'c'


        return -1;
    }

}
bool all_in_checker(History history){
    return false;
}

int get_betting_round(History history){
    return 0;
}
int main(){
    printf("Hello World");
}