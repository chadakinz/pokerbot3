#ifndef ATTR_H
#define ATTR_H
#include "commonIncludes.h"
#include <type_traits>
#include <span>
#include <algorithm>
#include <set>

Deck chance_sample(int cards, const Deck& deck);
std::vector<double> normalize_over_actions(const std::vector<double>& regret_matrix);
std::vector<double> get_hand_distribution();
std::vector<double> span_subtract(std::span<double> s, std::vector<double> v);
void process_distribution(const Config& game_info, std::vector<double>& p1_distribution, std::vector<double>& p2_distribution);
std::vector<double> update_distribution(const std::vector<double>& dist, const std::span<double>& strategy_a_I);


struct CharSetKey {
    std::string canonical;

    CharSetKey(const std::string& s) {
        std::set<char> unique_chars(s.begin(), s.end());
        canonical = std::string(unique_chars.begin(), unique_chars.end());
    }

    // Needed for equality check in unordered_map
    bool operator==(const CharSetKey& other) const {
        return canonical == other.canonical;
    }
};


struct VectorHash {
    template<typename T>
    std::size_t operator()(const std::vector<T>& myvec) const {
        std::size_t hash = myvec.size();
        for (const T& val: myvec){
            hash ^= std::hash<T>()(val) + 0x9e3779b9 + (hash << 6) + (hash >> 2);
        }
        return hash;
    }
};

inline void hash_combine(std::size_t& seed, std::size_t h) {
    seed ^= h + 0x9e3779b9 + (seed << 6) + (seed >> 2);
}

// Hash function
struct VectorTupleHash {
    std::size_t operator()(const std::vector<std::tuple<int, char, int>>& vec) const {
        std::size_t seed = 0;
        for (const auto& tup : vec) {
            std::size_t h1 = std::hash<int>{}(std::get<0>(tup));
            std::size_t h2 = std::hash<char>{}(std::get<1>(tup));
            std::size_t h3 = std::hash<int>{}(std::get<2>(tup));
            hash_combine(seed, h1);
            hash_combine(seed, h2);
            hash_combine(seed, h3);
        }
        return seed;
    }
};
template<typename T>
requires std::is_arithmetic_v<T>
inline std::vector<T> operator*(const std::vector<T>& a, const std::vector<T>& b){
    if (a.size() != b.size()){
        throw std::invalid_argument("Vectors need to be the same size");
    }
    std::vector<T> c(a.size());
    for (size_t i = 0; i < a.size(); i++){
        c[i] = (a[i] * b[i]);
    }
    return c;
}

template<typename T, std::size_t N>
requires std::is_arithmetic_v<T>
inline std::array<T, N> operator*(const std::array<T, N>& a, const std::array<T, N>& b) {

    std::array<T, N> c;
    std::transform(a.begin(), a.end(), b.begin(), c.begin(), std::multiplies<T>());

    return c;
}

template<typename T, std::size_t N>
requires std::is_arithmetic_v<T>
inline std::array<T, N> operator+(const std::array<T, N>& a, const std::array<T, N>& b) {

    std::array<T, N> c;
    std::transform(a.begin(), a.end(), b.begin(), c.begin(), std::plus<T>());

    return c;
}


template<typename T>
requires std::is_arithmetic_v<T>
inline std::vector<T> operator+(const std::vector<T>& a, const std::vector<T>& b){
    if (a.size() != b.size()){
        throw std::invalid_argument("Vectors need to be the same size");
    }
    std::vector<T> c(a.size());
    for (size_t i = 0; i < a.size(); i++){
        c[i] = (a[i] + b[i]);
    }
    return c;
}

template<typename T, std::size_t N>
requires std::is_arithmetic_v<T>
inline std::array<T, N> operator-(const std::array<T, N>& a, const std::array<T, N>& b) {

    std::array<T, N> c{};
    std::transform(a.begin(), a.end(), b.begin(), c.begin(), std::minus<T>());

    return c;
}

template<typename T>
requires std::is_arithmetic_v<T>
inline std::vector<T> operator-(const std::vector<T>& a, const std::vector<T>& b){
    if (a.size() != b.size()){
        throw std::invalid_argument("Vectors need to be the same size");
    }
    std::vector<T> c(a.size());
    for (size_t i = 0; i < a.size(); i++){
        c[i] = (a[i] - b[i]);
    }
    return c;
}

template <typename Container>
requires std::is_arithmetic_v<typename Container::value_type>
double vector_sum(const Container& v) {
    double sum = 0;
    for (const auto& val : v) {
        sum += val;
    }
    return sum;
}

template <typename Container>
requires std::is_arithmetic_v<typename Container::value_type>
double vector_positive_sum(const Container& v)
{
    double sum = 0.0;
    for (const auto& val: v){
        if (val > 0.0) {
            sum += val;
        }
    }
    return sum;
}
template <typename T>
class Regret_Cache: public std::unordered_map<std::vector<T>, std::vector<double>, VectorTupleHash> {
size_t vector_size;
public:
Regret_Cache(size_t n) : vector_size(n) {}
std::vector<double>& operator[](const std::vector<T>& key){
    auto it = (*this).find(key);
    if (it == (*this).end()){
        auto pair = (*this).emplace(key, std::vector(vector_size * config_nums["NUM_HANDS"] , 0.0));
        return (*pair.first).second;
    }
    else{
        return (*it).second;
    }
}
std::span<double> get_regret_for_hand(std::vector<double>& matrix, int i){
    return std::span(matrix).subspan(vector_size * i, vector_size);
}

std::vector<double> get_strategy(const std::vector<T>& key){
    std::vector<double> strategy_matrix(config_nums["NUM_HANDS"] * vector_size);
    std::vector<double>& regret_hand_matrix = (*this)[key];
    double norm_sum;
    std::span<double> regret_for_hand;
    for (int i = 0; i < config_nums["NUM_HANDS"] ; i++){
        regret_for_hand = get_regret_for_hand(regret_hand_matrix, i);
        norm_sum = vector_positive_sum(regret_for_hand);

        if (norm_sum <= 0.0){
            for (int j = 0; j< vector_size; j++){
                strategy_matrix[vector_size * i  + j] = 1.0/vector_size;
            }
        }
        else {
            for (int j = 0; j < vector_size; j++) {
                strategy_matrix[vector_size * i + j] = std::max(regret_for_hand[j], 0.0) / norm_sum;
            }
        }
    }
    return strategy_matrix;
}
};

template <typename T>
std::array<double, NUM_HANDS> get_cumulative_regret(Regret_Cache<T>& cache) {
    std::array<double, NUM_HANDS> cumulative_regret;
    cumulative_regret.fill(0.0);

    std::vector<double> placeholder(config_nums["NUM_HANDS"], 0.0);

    for (const auto& [key, value] : cache) {
        placeholder = placeholder + normalize_over_actions(value);
    }

    for (int i = 0; i < config_nums["NUM_HANDS"]; i++) {
        cumulative_regret[i] = placeholder[i];
    }
    //printf("cumulative_regret at 0: %f\n", cumulative_regret[0]);

    return cumulative_regret;
}

#endif