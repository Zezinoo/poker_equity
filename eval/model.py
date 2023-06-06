import docplex.mp.model as cpx


opt_model = cpx.Model(name="AVGERROR Model")
# Parameters
N_FEATURES = 10
m = 19600  # Number of Flops
n = 73  # Number of Features


# Decision Variables
#
# epsilon_i for each flop i, the error estimating it
# x_j the weight of each feature in the estimation
# y_j binary variable that determines if some constraint j is utilized or not

# epsilon is real nonnegative

eps_vars = {(i): opt_model.semicontinuous_var(
    lb=0, name="eps_{0}".format(i)) for i in range(m)}

# x_j is real , and a probability

x_vars = {(j): opt_model.continuous_var(
    lb=-1, ub=1, name="x_{0}".format(j)) for j in range(n)}
# y_j is binary
y_vars = {(j): opt_model.integer_var(lb=0, ub=N_FEATURES,
                                     name="y_{0}".format(j)) for j in range(n)}

# <= constraints
xy_leq_constraints = {j:
                      opt_model.add_constraint(
                          ct=x_vars[j] <= y_vars[j],
                          ctname="xy_cstr{0}".format(j))
                      for j in range(n)
                      }
y_leq_constraints = {j:
                     opt_model.add_constraint(
                         ct=y_vars[j] <= N_FEATURES,
                         ctname="y_cstr{0}".format(j))
                     for j in range(n)}
eps_leq_constraints = {i:
                       opt.model.add_constraint(

                       )}
