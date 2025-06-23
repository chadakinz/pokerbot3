#include "include/commonIncludes.h"
#include "include/attr.h"

Deck chance_sample(int num_cards, const Deck& deck){
    int n = deck.size();
    int num;
    std::uniform_int_distribution<> dist(0,  n- 1);
    int sampled_num = dist(gen);
    Deck cards;
    for (int i = 0; i < num_cards; i++){
        num = (sampled_num + i) % n;
        cards.emplace_back(deck[num]);
    }
    return cards;
}
