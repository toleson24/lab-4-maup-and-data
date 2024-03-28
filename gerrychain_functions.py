import matplotlib.pyplot as plt
from gerrychain import Graph, Partition, proposals, updaters, constraints, accept, MarkovChain, Election, \
    GeographicPartition
from gerrychain.updaters import cut_edges, Tally
from gerrychain.proposals import recom
from gerrychain.accept import always_accept
from functools import partial


def dem_win_updater(partition):
    dem_shares = partition["PRES20"].percents("Democratic")
    dem_wins = 0
    for dist in dem_shares:
        if dist > 0.5:
            dem_wins += 1
    return dem_wins


def init_partition(graph,
                    assignment="CD", election_name="PRES20",
                    dem_col_name="G20PRED",
                    rep_col_name="G20PRED",
                    pop_col_name="TOTPOP"):
    # Initialize updaters
    my_updaters = {
        "our cut edges": cut_edges,
        "district population": Tally(pop_col_name, alias="district population"),
        "HISP": Tally("HISP", alias="HISP")
    }
    e = Election(election_name, {"Democratic": dem_col_name, "Republican": rep_col_name})
    my_updaters.update({e.name: e})
    initial_partition = GeographicPartition(
        graph,
        assignment=assignment,  # Congressional Districting
        updaters=my_updaters
    )
    return initial_partition


def calc_population(graph, num_dist, pop_col_name):
    tot_pop = sum([graph.nodes()[v][pop_col_name] for v in graph.nodes()])
    return tot_pop / num_dist


def init_markov_chain(graph, initial_partition, pop_col_name, ideal_pop, steps, pop_tolerance=0.02):
    # Set up Markov Chain initializers
    rw_proposal = partial(recom,
                          pop_col=pop_col_name,
                          pop_target=ideal_pop,
                          epsilon=pop_tolerance,
                          node_repeats=1
                          )
    population_constraint = constraints.within_percent_of_ideal_population(
        initial_partition,
        pop_tolerance,
        pop_key="district population")
    our_random_walk = MarkovChain(
        proposal=rw_proposal,
        constraints=[population_constraint],
        accept=always_accept,
        initial_state=initial_partition,
        total_steps=steps)
    return our_random_walk


def walk_the_run(random_walk, num_dist, cutedge_ensemble, lmaj_ensemble, dem_win_ensemble):
    print("walking the ensemble")
    for part in random_walk:
        # Walk randomly
        cutedge_ensemble.append(len(part["our cut edges"]))

        num_maj_latino = 0
        for i in range(num_dist):
            l_perc = part["HISP"][i] / part["district population"][i]
            if l_perc >= 0.5:
                num_maj_latino = num_maj_latino + 1
        lmaj_ensemble.append(num_maj_latino)
        dem_win_ensemble.append(dem_win_updater(part))

    return cutedge_ensemble, lmaj_ensemble, dem_win_ensemble


def plot_histograms(ensemble, filename):
    plt.figure()
    plt.hist(ensemble, align="left")
    plt.savefig(filename)
