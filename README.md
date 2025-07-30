### Quick Start Commands

# Train the agent on paper_map (main experiment)

```bash
python3 main.py --mode train --phase1-episodes 10000 --phase2-episodes 10000 --save saved/paper_map.pkl --map paper_map

python3 main.py --mode train --phase1-episodes 10000 --phase2-episodes 10000 --save saved/paper_map_12.pkl --map paper_map --seed 12

python3 main.py --mode train --phase1-episodes 10000 --phase2-episodes 10000 --save saved/paper_map_22.pkl --map paper_map --seed 22

python3 main.py --mode train --phase1-episodes 10000 --phase2-episodes 10000 --save saved/paper_map_32.pkl --map paper_map --seed 32

python3 main.py --mode train --phase1-episodes 10000 --phase2-episodes 10000 --save saved/paper_map_42.pkl --map paper_map --seed 42

python3 main.py --mode train --phase1-episodes 10000 --phase2-episodes 10000 --save saved/paper_map_52.pkl --map paper_map --seed 52
```

# Visualize the trained agent

```bash
python3 main.py --mode visualize --load saved/paper_map.pkl --map paper_map
```

# Other example commands

```bash
python3 main.py --mode train --phase1-episodes 10000 --phase2-episodes 10000 --save saved/simple_map4.pkl --map simple_map4
python3 main.py --mode visualize --load saved/simple_map4.pkl --map simple_map4
python3 main.py --mode train --phase1-episodes 1000 --phase2-episodes 1000 --save saved/q_values.pkl --map team_map
python3 main.py --mode visualize --load saved/q_values_simple_map.pkl --map simple_map --delay 200
```

# Two-Timescale Goal-Based IQL in a Custom Grid Environment

## Overview

This project implements a Two-Timescale Goal-Based Independent Q-Learning (IQL) algorithm in a custom grid environment. The environment is designed using the `PettingZoo` library and rendered with `pygame`. The agents in the environment are a **robot** and a **human**, and the robot's goal is to maximize the human's potential to achieve various goals.

The algorithm follows a two-phase approach:

- **Phase 1**: Learn cautious human behavior models while the robot acts pessimistically
- **Phase 2**: Learn an optimal robot policy using the learned human models

## Environment Description

The environment is a grid-based world with the following elements:

- **Walls (`#`)**: Impassable obstacles.
- **Goal (`G`)**: The target location for the human.
- **Key (`K`)**: An object that may be required to unlock doors.
- **Door (`D`)**: A barrier that can be opened with a key.
- **Lava (`L`)**: Hazardous tiles that terminate the episode if stepped on.
- **Robot (`R`)**: The learning agent controlled by the IQL algorithm.
- **Human (`H`)**: A simulated agent with predefined behavior.

## Actions

The environment supports the following actions, similar to MiniGrid:

| Action | Name   | Description               |
| ------ | ------ | ------------------------- |
| 0      | Left   | Move left                 |
| 1      | Right  | Move right                |
| 2      | Up     | Move up                   |
| 3      | Down   | Move down                 |
| 4      | Pickup | Pick up an object         |
| 5      | Drop   | Drop an object            |
| 6      | Toggle | Toggle/activate an object |
| 7      | No-op  | Do nothing                |

### Objects

The environment includes the following objects, rendered similarly to MiniGrid:

- **Walls**: Impassable obstacles.
- **Goal**: The target location for the agent.
- **Key**: An object required to unlock doors.
- **Door**: A barrier that can be opened with a key.
- **Lava**: Hazardous tiles that terminate the episode if stepped on.
- **Ball**: A movable object.
- **Box**: A container that may hold other objects.

## Possible Actions

The environment supports the following actions:

- move_up
- move_down
- move_left
- move_right

### Rendering

The environment is rendered using `pygame`. The grid elements are displayed with distinct colors:

- **Walls**: Black
- **Goal**: Green
- **Key**: Yellow
- **Door**: Brown
- **Lava**: Red
- **Robot**: Blue
- **Human**: Magenta

## Algorithm

The Two-Timescale Goal-Based Independent Q-Learning (IQL) algorithm is implemented with the following key features:

### Phase 1: Learning Human Behavior Models

- **Human Policy**: ε-greedy with ε_h decreasing from 0.5 to ε_h_0
- **Robot Policy**: Pessimistic policy that assumes worst-case human outcomes
- **Goal**: Learn conservative estimates of human Q-values Q_h^m
- **Updates**: Conservative Q-learning for humans, pessimistic action selection for robot

### Phase 2: Learning Robot Policy

- **Human Policy**: ε_h_0-greedy policy using learned Q_h^m
- **Robot Policy**: β_r-softmax with β_r increasing from 0.1 to β_r_0
- **Goal**: Learn optimal robot policy Q_r to maximize human potential
- **Updates**: Standard Q-learning for robot, minimal updates for humans

**Key Parameters:**

- Learning rates: `alpha_m` (Phase 1 human), `alpha_e` (Phase 2 human), `alpha_r` (robot)
- Discount factors: `gamma_h`, `gamma_r`
- Human exploration: `epsilon_h` (current, starts at 0.5), `epsilon_h_0` (target, final epsilon for converged policy)
- Set of possible human goals: `G`
- Prior probability distribution over goals: `mu_g`
- Probability of goal change per step: `p_g`
- Power function exponent: `eta`

## Gridworld Application of IQL

This section details the specific application of the IQL algorithm within the custom gridworld environment.

- **Actions ($a_r, a_h$):** Discrete actions available to the robot and human. Examples include:
  - Wait
  - Pickup (item)
  - Interact (e.g., toggle a switch, open a door)
- **Goals ($\mathcal{G}$):** The set of potential goals for the human.
  - Example: A predefined subset of grid cells that the human might want to reach, e.g., $\mathcal{G} = \{(x_1, y_1), (x_2, y_2), \dots\}$.
- **Goal Prior ($\mu_g$):** The assumed probability distribution over the set of goals $\mathcal{G}$.
  - Example: A uniform distribution, $\mu_g(g) = 1/|\mathcal{G}|$ for all $g \in \mathcal{G}$.
- **Base Human Reward ($r_h^{obs} = r_h(s, a_r, a_h, s', g)$):** This reward is provided by the environment simulator and signals the human's success in achieving their current goal $g$.
  - Example: If the human's goal $g$ is to reach cell $(x_g, y_g)$, then $r_h^{obs} = +1$ if the human's position in the next state $s'$ is $(x_g, y_g)$, and $0$ otherwise. A small negative penalty for each step taken (e.g., -0.01) can also be included.
  - For the "simplest case", $r_h(s, a_r, a_h, s', g) = 1_{s'=g}$ (reward of 1 for reaching state $g$).
- **Robot's Reward ($r_r$):** This reward is calculated internally by the robot, not provided by the environment. It is based on the human's expected future value, averaged over potential goals, possibly transformed by a function $f$ and an exponent $\eta$.
  - It is typically formulated as $r_r = f(\mathbb{E}_{g' \sim \mu_g} [\hat{V}_h(s', g')^{1+\eta}])$, where $\hat{V}_h(s', g')$ is the learned value function for the human achieving goal $g'$ from state $s'$. The expectation $\mathbb{E}_{g' \sim \mu_g} [\cdot]$ is the $r_r^{calc}$ term from step 2.f.ii in the algorithm description.
- **Q-Tables:** The learning process involves maintaining two main Q-tables:
  - Robot's Q-table: $Q_r[s][a_r]$ of size $|\mathcal{S}| \times |\mathcal{A}_r|$.
  - Human's Q-table: $Q_h[s][g][a_h]$ of size $|\mathcal{S}| \times |\mathcal{G}| \times |\mathcal{A}_h|$.
- **Typical Parameters for Gridworld:**
  - Learning rates: `alpha_m ≈ 0.1`, `alpha_e ≈ 0.2`, `alpha_r ≈ 0.01`
  - Discount factors: `gamma_h = 0.99`, `gamma_r = 0.99`
  - Human exploration: `epsilon_h` starts at 0.5, decays to `epsilon_h_0 ∈ [0.05, 0.2]` (final exploration level)
  - Robot rationality: `beta_r` starts at 0.1, increases to `beta_r_0 ∈ [5, 20]` (higher = more deterministic)
  - Robot exploration: `epsilon_r` starts at 0.1, decays to 0.01 in Phase 1
  - Goal change probability: `p_g ≈ 0.01` for infrequent goal changes
  - Power exponent: `eta = 0` (linear) or `eta = 1` (quadratic emphasis)

### Hyperparameters

The key hyperparameters for the Two-Phase Timescale IQL algorithm are defined in `main.py` and `iql_timescale_algorithm.py`. Here are all the default values used in the implementation:

#### Core Learning Parameters (Set in main.py)

- **`alpha_m`**: `0.1` (Phase 1 learning rate for human models)
- **`alpha_e`**: `0.1` (Phase 2 fast timescale learning rate for human models)
- **`alpha_r`**: `0.1` (Robot learning rate)
- **`gamma_h`**: `0.99` (Human's discount factor)
- **`gamma_r`**: `0.99` (Robot's discount factor)

#### Exploration and Policy Parameters

- **`beta_r_0`**: `5.0` (Target robot softmax temperature for Phase 2 - set in main.py)
- **`beta_r`**: `0.1` (Initial robot softmax temperature, increases to `beta_r_0` - set internally)
- **`epsilon_h_0`**: `0.1` (Final human epsilon-greedy parameter - set in main.py)
- **`epsilon_h`**: `0.8` (Initial human epsilon-greedy parameter, decreases to `epsilon_h_0` - set internally)
- **`epsilon_r`**: `1.0` (Robot exploration in Phase 1 - set in main.py)

#### Goal and Environment Parameters

- **`p_g`**: `0.01` (Probability of goal change per step - set in main.py)
- **`eta`**: `0.1` (Power parameter for robot reward function - set in main.py)
- **`zeta`**: `1.0` (Power parameter in X_h(s) calculation - default in class constructor)
- **`xi`**: `1.0` (Power parameter in U_r(s) calculation - default in class constructor)

#### Exploration Bonus Parameters (Set internally in class)

- **`exploration_bonus_initial`**: `50.0` (Initial exploration bonus for robot)
- **`exploration_bonus_decay`**: `0.995` (Decay rate for robot exploration bonus)
- **`human_exploration_bonus_initial`**: `75.0` (Initial exploration bonus for humans)
- **`human_exploration_bonus_decay`**: `0.998` (Decay rate for human exploration bonus)

#### Convergence Monitoring (Set internally in class)

- **`convergence_threshold`**: `1e-4` (Threshold for Q-value changes)
- **`convergence_window`**: `100` (Episodes to check for convergence)

#### Action Spaces (Hard-coded in main.py)

- **Robot actions**: `[0, 1, 2, 3, 4, 5, 6]` (Left, Right, Up, Down, Pickup, Drop, Toggle)
- **Human actions**: `[0, 1, 2, 6]` (Left, Right, Up, No-op)

#### Command-line Configurable Parameters

- **`reward_function`**: `'power'` (Robot reward function type - default in argparse)
- **`concavity_param`**: `1.0` (Concavity parameter for generalized bounded function - default in argparse)
- **`seed`**: `42` (Random seed for reproducibility - default in argparse)

The environment and algorithm use a fixed random seed of **42** (`np.random.seed(42)` and `random.seed(42)`) to ensure results are reproducible across runs. This setting is applied by default when resetting the environment.

This section details the specific application of the IQL algorithm within the custom gridworld environment.

- **Actions (`a_r`, `a_h`)**: Discrete actions available to the robot and human. Examples include:

  - Wait
  - Pickup (item)
  - Interact (e.g., toggle a switch, open a door)

- **Goals (`G`)**: The set of potential goals for the human.

  - Example: A predefined subset of grid cells that the human might want to reach, e.g., `G = {(x1, y1), (x2, y2), ...}`.

- **Goal Prior (`mu_g`)**: The assumed probability distribution over the set of goals `G`.

  - Example: A uniform distribution, `mu_g(g) = 1 / |G|` for all `g` in `G`.

- **Base Human Reward (`r_h_obs = r_h(s, a_r, a_h, s', g)`)**: This reward is provided by the environment simulator and signals the human's success in achieving their current goal `g`.

  - Example: If the human's goal `g` is to reach cell `(x_g, y_g)`, then `r_h_obs = +1` if the human's position in the next state `s'` is `(x_g, y_g)`, and `0` otherwise. A small negative penalty for each step taken (e.g., `-0.01`) can also be included.
  - For the simplest case: `r_h(s, a_r, a_h, s', g) = 1 if s' == g else 0` (reward of 1 for reaching state `g`).

- **Robot's Reward (`r_r`)**: This reward is calculated internally by the robot, not provided by the environment. It is based on the human's expected future value, averaged over potential goals, possibly transformed by a function `f` and an exponent `eta`.

  - General formula: `r_r = f(E_{g' ~ mu_g}[V_h_hat(s', g') ** (1 + eta)])`
    - `V_h_hat(s', g')` is the learned value function for the human achieving goal `g'` from state `s'`
    - `mu_g` is the prior distribution over goals
    - `eta` is the power/exponent parameter
    - `f` is a transformation function (often identity or power)
    - `E_{g' ~ mu_g}[...]` denotes expectation over possible goals
    - The expectation is the `r_r_calc` term from step 2.f.ii in the algorithm description.

- **Q-Tables:** The learning process involves maintaining two main Q-tables:

  - Robot's Q-table: `Q_r[s][a_r]` of size `|S| x |A_r|`
  - Human's Q-table: `Q_h[s][g][a_h]` of size `|S| x |G| x |A_h|`

  - Example: If the human's goal $g$ is to reach cell $(x_g, y_g)$, then $r_h^{obs} = +1$ if the human's position in the next state $s'$ is $(x_g, y_g)$, and $0$ otherwise. A small negative penalty for each step taken (e.g., -0.01) can also be included.
  - For the simplest case: $r_h(s, a_r, a_h, s', g) = \mathbb{I}[s' = g]$ (reward of 1 for reaching state $g$).

- **Robot's Reward ($r_r$):**
  This reward is calculated internally by the robot (not provided by the environment). It is based on the human's expected future value, averaged over possible goals, and may be transformed by a function $f$ and exponent $\eta$.

  - **General formula:**
    ```math
    r_r = f\left(\mathbb{E}_{g' \sim \mu_g} [\hat{V}_h(s', g')^{1+\eta}]\right)
    ```
    where:
    - $\hat{V}_h(s', g')$ is the learned value function for the human achieving goal $g'$ from state $s'$
    - $\mu_g$ is the prior distribution over goals
    - $\eta$ is the power/exponent parameter
    - $f$ is a transformation function (often identity or power)
    - $\mathbb{E}_{g' \sim \mu_g}[\cdot]$ denotes expectation over possible goals
    - The expectation $\mathbb{E}_{g' \sim \mu_g}[\cdot]$ is the $r_r^{calc}$ term from step 2.f.ii in the algorithm description.

- **Q-Tables:**
  The learning process maintains two main Q-tables:

  - **Robot's Q-table:**

    ```math
    Q_r[s][a_r] \text{ of size } |\mathcal{S}| \times |\mathcal{A}_r|
    ```

    - $s$: state
    - $a_r$: robot action
    - $|\mathcal{S}|$: number of possible states
    - $|\mathcal{A}_r|$: number of robot actions

  - **Human's Q-table:**
    ```math
    Q_h[s][g][a_h] \text{ of size } |\mathcal{S}| \times |\mathcal{G}| \times |\mathcal{A}_h|
    ```
    - $s$: state
    - $g$: human goal
    - $a_h$: human action
    - $|\mathcal{G}|$: number of possible goals
    - $|\mathcal{A}_h|$: number of human actions

This ensures that training runs with the same seed will produce identical results, making experiments reproducible and results comparable.

## Code Structure

- **`env.py`**: Defines the custom grid environment.
- **`iql_timescale_algorithm.py`**: Implements the Two-Timescale Goal-Based IQL algorithm.
- **`main.py`**: Runs the training loop and renders the environment.
- **`trained_agent.py`**: Implements an agent that uses saved Q-values for deterministic visualization.
- **`envs/`**: Contains map definitions for different grid layouts:
  - **`map_loader.py`**: Utility functions for loading map layouts.

Maps are defined as a list of strings, where each character represents a specific element in the grid:

- **`G`**: Goal
- **`L`**: Lava (hazardous tile)

### Available Maps

- **`paper_map`**: The main experimental map where the human is trapped in a 1x1 room and the robot must open the door.
- **`simple_map`**: A small, simple layout with a door separating the robot and human from the goal.
- **`simple_map4`**: A variation of the simple map with different key/door positioning.
- **`complex_map`**: A larger, more complex layout with multiple rooms and hazards.
- **`team_map`**: A multi-human environment with different goals for each human.
- **`collaborator_map`**: A collaborative environment with boxes and multiple humans.

## Running the Code

1. Install the required dependencies:

   ```bash
   pip3 install -r requirements.txt
   ```

2. Train the IQL algorithm on the paper_map (recommended):

   ```bash
   python3 main.py --mode train --phase1-episodes 10000 --phase2-episodes 10000 --save saved/paper_map.pkl --map paper_map
   ```

   Or train on other maps:

   ```bash
   python3 main.py --mode train --episodes 100 --save saved/q_values.pkl --map simple_map
   ```

   ```bash
   python3 main.py --mode train --episodes 100 --save saved/q_values.pkl --map collaborator_map --render
   ```

3. Visualize the trained agent:

   ```bash
   python3 main.py --mode visualize --load saved/paper_map.pkl --map paper_map
   ```

   Or visualize other trained models:

   ```bash
   The following command-line arguments are available:
   ```

- `--mode`: Choose between `train` (train the model), `visualize` (run trained model), or `test` (run deterministic test). Default: `train`.
- `--save`: Path to save trained Q-values. Default: `saved/q_values.pkl`.
- `--load`: Path to load trained Q-values for visualization. Default: `saved/q_values.pkl`.
- `--episodes`: Number of episodes for training. Default: `1000`.
- `--phase1-episodes`: Number of episodes for Phase 1 (timescale algorithm only). Default: `500`.
- `--phase2-episodes`: Number of episodes for Phase 2 (timescale algorithm only). Default: `500`.
- `--delay`: Delay in milliseconds between steps during visualization. Default: `100`.

1. **Training**: The agent is trained in deterministic=false mode for a specified number of episodes.
2. **Saving**: After training, Q-values are saved to the specified file.
3. **Visualization**: The trained Q-values can be loaded and used to visualize the agent's behavior in deterministic mode.

## Future Work

- Add more complex human behaviors.
- Introduce additional grid elements and interactions.
- Experiment with different reward functions and learning rates.
- Implement convergence metrics to automatically determine when training should stop.
- Create more diverse map layouts for different training scenarios.
