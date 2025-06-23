#include <commonIncludes.h>
#include <attr.h>
#include <phevaluator/phevaluator.h>
#include <algorithm>
//std::get<x>(tuple) -->std::get<x>(std::get<player_action>(variant));

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
int get_potsize(History history){
    int potsize = 0;
    for(auto action = history.begin(); action != history.end(); action++){
        if (!std::holds_alternative<chance_action>(*action)){
            potsize += std::get<2>(std::get<player_action>(*action));

        }
    }

    return potsize;
}

int get_call_amount(History history){
    auto last_action = *history.rbegin();
    if (std::holds_alternative<chance_action>(last_action)) return 0;
    else return std::get<2>(std::get<player_action>(last_action));;
}

int get_chips(History history, int i){
    int chips;
    if (i == 1){
        chips = std::get<1>(std::get<player_action>(*(history.begin())));
    }else{
        chips = std::get<1>(std::get<player_action>(*(history.begin() + 1)));
    }
    for(auto action = history.begin(); action != history.end(); action++){
        if (!(std::holds_alternative<chance_action>(*action))){
            auto player = std::get<0>(*action);
            if (std::get<0>(std::get<player_action>(*action)) == i){
                chips -= std::get<2>(std::get<player_action>(*action));
            }

        }
    }
    return chips;
}

bool is_check(History history){
    bool check = false;
    for (auto it = history.rbegin() + 1; it != history.rend(); it ++){
        auto item = *it;
        if (std::holds_alternative<chance_action>(item)) break;
        if (std::get<1>(std::get<player_action>(item)) == 'R' || std::get<1>(std::get<player_action>(item)) == 'C') {
            check = true;
            break;
        }
    }
    return check;
}

int get_betting_round(History history){
    int count = 0;
    for(auto action = history.begin() + 7; action != history.end(); action++){
        if (std::holds_alternative<chance_action>(*action)) count ++;
    }
    return count;
}
Deck get_hand(History history, int i){
    Deck hand = {};
    Deck cards;
    if (i == 1){
        cards = std::get<1>(std::get<chance_action>(*(history.begin() + 2)));
        hand.emplace_back(cards[0]);
        hand.emplace_back(cards[1]);
    }else{
        cards = std::get<1>(std::get<chance_action>(*(history.begin() + 3)));
        hand.emplace_back(cards[0]);
        hand.emplace_back(cards[1]);
    }

    for(auto action = history.begin() + 7; action != history.end(); action++){
        if (std::holds_alternative<chance_action>(*action)){
            cards = std::get<1>(std::get<chance_action>(*action));
            hand.insert(hand.end(), cards.begin(), cards.end());

        }
    }
    return hand;
}

bool all_in_checker(History history){
    for(int i = 0; i != 4; i++){
        auto item = *(history.rbegin() + i);
        bool chance_action_b =  std::holds_alternative<chance_action>(item);
        if(!chance_action_b){
            if(std::get<1>(std::get<player_action>(item)) == 'A'){
                return true;
            }
        }
    }
    return false;
}

//WARNING: function doesnt check if history is on the last street
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
        auto last_player_act = std::get<0>(std::get<player_action>(last_action));
        auto last_val = std::get<1>(std::get<player_action>(last_action));
        bool check = is_check(history);

        if ((last_val == 'C') && check){
            return 'c';
        }else if ((last_val == 'C') && !check){
            return 2;
        }else if ((last_val == 'R') && last_player_act == 1){
            return 2;
        }
        else if (last_val == 'R' && last_player_act == 2){
            return 1;
        }

    }

}

bool is_terminal(History history){
    auto last_action = *(history.rbegin());
    bool chance_action_b =  std::holds_alternative<chance_action>(last_action);
    bool all_in = all_in_checker(history);
    bool last_street = get_betting_round(history) == 3;
    bool check = is_check(history);
    if (all_in && last_street) return true;
    else if (all_in && !last_street) return false;
    else if (chance_action_b) return false;
    auto last_val = std::get<1>(std::get<player_action>(last_action));
    if (last_val == 'F') return true;
    else if (!last_street) return false;
    else if (last_val == 'R') return false;
    else if (check && last_val == 'C') return true;
    else return false;

}


int utility(History history, int i){
    int chips;
    int opp_chips;
    int opp_id;
    auto last_action = *(history.rbegin());
    bool chance_action_b =  std::holds_alternative<chance_action>(last_action);



    if (i == 1){
        int opp_id = 2;
        int chips = std::get<1>(std::get<player_action>(* history.begin()));;
        int opp_chips = std::get<1>(std::get<player_action>(* (history.begin() + 1)));;

    }else{
        int opp_id = 1;
        int opp_chips = std::get<1>(std::get<player_action>(* history.begin()));;
        int chips = std::get<1>(std::get<player_action>(* (history.begin() + 1)));;
    }
    int chips_staked = chips - get_chips(history, i);
    int opp_chips_staked = opp_chips - get_chips(history, opp_id);


    if (!chance_action_b){
        auto last_player_act = std::get<0>(std::get<player_action>(last_action));
        auto last_val = std::get<1>(std::get<player_action>(last_action));
        if (last_val == 'F' && last_player_act == i){
            return -chips_staked;
        }else if (last_val == 'F' && last_player_act != i){
            return opp_chips_staked;
        }
    }

    std::vector<int> hand = process_hand(get_hand(history, i));
    std::vector<int> opp_hand = process_hand(get_hand(history, opp_id));
    int hero_score = evaluate_7cards(hand[0], hand[1], hand[2], hand[3], hand[4], hand[5], hand[6]);
    int opp_score = evaluate_7cards(opp_hand[0], opp_hand[1], opp_hand[2], opp_hand[3], opp_hand[4], opp_hand[5], opp_hand[6]);
    if (hero_score < opp_score){
        return opp_chips_staked;
    }else if (hero_score > opp_score){
        return -chips_staked;
    }else{
        return 0;
    }
}
History process_action(int num, const History& history, int i){
    int raise_amount;
    int opp_id;
    int call_amount = get_call_amount(history);
    int potsize = get_potsize(history);
    int chips = get_chips(history, i);
    if(i == 1) opp_id = 2;
    else opp_id = 1;
    int opp_chips = get_chips(history, opp_id);
    switch (num){
        case 0:
            return {player_action(i, 'F', 0)};
        case 1:
            if (chips <= call_amount) return {player_action(i, 'A', chips)};
            else return {player_action(i, 'C', call_amount)};
        case 2:
            if (chips <= call_amount) return {player_action(i, 'A', chips)};
            raise_amount = .25 * potsize;
            if (raise_amount < call_amount){
                return {player_action(i, 'C', call_amount), player_action(i, 'R',  std::min({chips - call_amount, call_amount, opp_chips}))};
            }else{
                return {player_action(i, 'C', call_amount), player_action(i, 'R',  std::min({chips - call_amount, raise_amount, opp_chips}))};
            }

        case 3:
            if (chips <= call_amount) return {player_action(i, 'A', chips)};
            raise_amount = .5 * potsize;
            if (raise_amount < call_amount){
                return {player_action(i, 'C', call_amount), player_action(i, 'R',  std::min({chips - call_amount, call_amount, opp_chips}))};
            }else{
                return {player_action(i, 'C', call_amount), player_action(i, 'R',  std::min({chips - call_amount, raise_amount, opp_chips}))};
            }

        case 4:
            if (chips <= call_amount) return {player_action(i, 'A', chips)};
            raise_amount = potsize;
            if (raise_amount < call_amount){
                return {player_action(i, 'C', call_amount), player_action(i, 'R',  std::min({chips - call_amount, call_amount, opp_chips}))};
            }else{
                return {player_action(i, 'C', call_amount), player_action(i, 'R',  std::min({chips - call_amount, raise_amount, opp_chips}))};
            }
        case 5:
            if (chips <= call_amount) return {player_action(i, 'A', chips)};
            raise_amount = chips - call_amount;
            return {player_action(i, 'C', call_amount), player_action(i, 'R',  std::min({chips - call_amount, raise_amount, opp_chips}))};
    }
}





//TODO finish function




int main(){
    printf("Hello World");
}
