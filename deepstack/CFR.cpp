#define CFR
#include <attr.hpp>
#include <commonIncludes.h>
#include <environment.h>
#include <testing_functions.hpp>
std::vector<double> traverse(const std::vector<double>& p1_distribution, const std::vector<double>& p2_distribution,
                             const Config& game_info, const History current_history, const int current_player, const int traversing_player, Regret_Cache<action>& cache){

    std::vector<double> counter_factual_value_A;
    std::vector<double> counter_factual_matrix;
    std::vector<double> regret_matrix;
    std::span<double> counter_factual_value_A_span;
    std::vector<double> regret_A, p1_updated_distribution, p2_updated_distribution;
    std::vector<double> counter_factual_value_I;
    History infoset;
    History next_history;
    std::span<double> action_prob;
    //printf("Current player: %d\n", current_player);
    //print_history(current_history);
    if (is_terminal(current_history)){
        if (traversing_player == 1){
            return utility(game_info, current_history, traversing_player, p1_distribution, p2_distribution);
        }else{
            return utility(game_info, current_history, traversing_player, p2_distribution, p1_distribution);
        }

    }

    infoset = current_history;

    std::vector<double> strategy_vec = cache.get_strategy(infoset);
    //print_vector(strategy_vec);
    std::span<double> strategy(strategy_vec);

    for (int action = 0; action < config_nums["num_actions"]; action++) {

        next_history = process_action(action, game_info, current_history, current_player);
        if (current_player == 1){
            //TODO bug is here >>>> <<<<<

            action_prob = strategy.subspan(action * config_nums["NUM_HANDS"], config_nums["NUM_HANDS"]);

            //print_container(action_prob);
            p1_updated_distribution = update_distribution(p1_distribution, action_prob);

            counter_factual_value_A = traverse(p1_updated_distribution, p2_distribution, game_info, next_history,
                                                                 get_next_turn(next_history), traversing_player, cache);


            //printf("Issue2\n\n");
        }else{

            action_prob = strategy.subspan(action * config_nums["NUM_HANDS"], config_nums["NUM_HANDS"]);
            p2_updated_distribution = update_distribution(p2_distribution, action_prob);
            counter_factual_value_A = traverse(p1_distribution, p2_updated_distribution, game_info, next_history,
                                                                 get_next_turn(next_history), traversing_player, cache);
            //printf("Counterfactual Value of 0 %f\n", counter_factual_value_A[0]);
            //printf("Issue2.1\n\n");
        }
        //printf("Check 1\n");
        //print_container(counter_factual_value_A);
        counter_factual_matrix.insert(counter_factual_matrix.begin() + (action * config_nums["NUM_HANDS"]),
                                      counter_factual_value_A.begin(), counter_factual_value_A.end());
        //printf("SIze of counterfactual matrix: %d\n", counter_factual_matrix.size());

    }


    std::vector<double> cfvIh = cache.get_strategy(infoset) * counter_factual_matrix;
    //print_container(counter_factual_matrix);
    //printf("Check 3\n");
    //printf("\n\n\n");
    //print_container(cfvIh);
    counter_factual_value_I = normalize_over_actions(cfvIh);
    //print_container(counter_factual_value_I);
    //exit(-1);
    if (traversing_player == current_player){
        for (int action = 0; action < config_nums["num_actions"]; action++){
            counter_factual_value_A_span = std::span(counter_factual_matrix).subspan(action * config_nums["NUM_HANDS"], config_nums["NUM_HANDS"]);
            //printf("Check 5\n");
            regret_A = span_subtract(counter_factual_value_A_span, counter_factual_value_I);
            //printf("Counterfactual Value of 0 %f\n", regret_A[0]);
            regret_matrix.insert(regret_matrix.begin() + action*config_nums["NUM_HANDS"], regret_A.begin(), regret_A.end());
        }
        cache[infoset] = cache[infoset] + regret_matrix;
        print_container(cache[infoset]);
        printf("size of cache[infoset] %d", cache[infoset].size());
        exit(-1);
    }

    return counter_factual_value_I;
}



int main(){
    std::vector<double> p1_distribution, p2_distribution;
    double frac;
    std::array<double, NUM_HANDS> weights;
    History root_node = {};
    std::vector<std::array<double, NUM_HANDS>> regret_time_series(config_nums["cfr_iterations"]);
    std::vector<std::array<double, NUM_HANDS>> dr_dt;
    std::array<double, NUM_HANDS> average_dr_dt;
    for(int i = 0; i < config_nums["num_samples"]; i++){
        Regret_Cache<action> cache(config_nums["num_actions"]);
        p1_distribution = get_hand_distribution();
        p2_distribution = get_hand_distribution();
        Config game_info = river_generator(config_nums["max_chip_amount"]);
        process_distribution(game_info, p1_distribution, p2_distribution);
        printf("Potsize: %d, chips: 1: %d, 2: %d\n", get_potsize(game_info, {}), get_chips(game_info, {}, 1), get_chips(game_info, {}, 2));
        for (int t = 1; t < config_nums["cfr_iterations"] + 1; t++){
            for(int i = 1; i < 3; i++){
                traverse(p1_distribution, p2_distribution, game_info, root_node, get_next_turn(root_node), i, cache);
            }
            frac = 1.0/(t);
            weights.fill(frac);
            regret_time_series[t - 1] = weights * get_cumulative_regret(cache);
            //printf("Time series at time t: %d ", t);
            //printf("regret_time_series[t-1] %f for i %d\n", regret_time_series[t- 1][0], 0);
        }

        dr_dt = derivative_cum_regret_over_time(regret_time_series);
        //print_vector_of_arrays(dr_dt);

        average_dr_dt = get_average_derivative_cum_regret_over_time(dr_dt);
        //print_container(average_dr_dt);
    }
    return 0;
}