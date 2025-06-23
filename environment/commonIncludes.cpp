#include "include/commonIncludes.h"
std::vector<std::string> ranks = {"2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"};
std::vector<std::string> suits = {"s", "d", "c", "h"};
std::random_device rd;
std::mt19937 gen(rd());
Deck sharedDeck;
void initializeSharedDeck() {
    for (const auto& suit : suits) {
        for (const auto& rank : ranks) {
            sharedDeck.emplace_back(rank + suit);
        }
    }
}
