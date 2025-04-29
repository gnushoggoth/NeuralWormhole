import random
import time
import string
import statistics # For mean and stdev

# --- Experiment Parameters ---
# Hive Mind Structure
NUM_MINDS = 5          # Number of processing units in the hive mind

# Task Parameters
STRING_LENGTH = 100
TARGET_CHAR = 'X'

# Timing & Processing Parameters (Simulated)
# Base time for one mind unit to process (find 'X') without distraction
BASE_TIME_MEAN = 5.0   # seconds
BASE_TIME_STDDEV = 1.0 # seconds (variability between units/trials)

# Distraction Parameters
DISTRACTION_PROB_PER_MIND = 0.4 # Chance *each mind* is affected by a distraction event
DISTRACTION_TIME_PENALTY = 3.0 # Extra seconds added if a mind is distracted

# Commanding Attention Parameters
# How much a "High Priority" command reduces the *impact* (penalty) of distraction
# 1.0 = no effect, 0.5 = halves penalty, 0.0 = eliminates penalty
HIGH_PRIORITY_DISTRACTION_MITIGATION = 0.2

# Experiment Structure
NUM_TRIALS_PER_CONDITION = 5

# --- Helper Functions ---

def generate_stimulus(length, target):
    """Generates a random string containing the target character exactly once."""
    # (Same as before)
    if length < 1: return "", -1
    chars = list(string.ascii_uppercase.replace(target, ''))
    random_chars = random.choices(chars, k=length - 1)
    insert_pos = random.randint(0, length - 1)
    stimulus_list = random_chars[:insert_pos] + [target] + random_chars[insert_pos:]
    return "".join(stimulus_list), insert_pos

def simulate_mind_unit_processing(is_distraction_condition, is_high_priority):
    """Simulates the time taken for a single mind unit to process the task."""
    # 1. Base processing time
    base_time = max(0.1, random.normalvariate(BASE_TIME_MEAN, BASE_TIME_STDDEV)) # Ensure time > 0

    # 2. Check for distraction (if applicable)
    time_penalty = 0
    is_distracted = False
    if is_distraction_condition:
        if random.random() < DISTRACTION_PROB_PER_MIND:
            is_distracted = True
            penalty = DISTRACTION_TIME_PENALTY
            # 3. Apply command effect (mitigation)
            if is_high_priority:
                penalty *= (1.0 - HIGH_PRIORITY_DISTRACTION_MITIGATION)
            time_penalty = penalty

    total_time = base_time + time_penalty
    return total_time, is_distracted

def run_hive_trial(condition, num_minds):
    """Runs a single trial for the hive mind under a given condition."""
    stimulus_string, correct_index = generate_stimulus(STRING_LENGTH, TARGET_CHAR)

    print("-" * 50)
    print(f"Condition: {condition.upper()}")
    print(f"Task: Hive Mind ({num_minds} units) find index of '{TARGET_CHAR}'.")
    # print("Stimulus:", stimulus_string) # Optional: Show the string

    individual_mind_times = []
    distracted_minds_count = 0

    # Determine condition flags
    is_distraction_condition = 'distraction' in condition
    is_high_priority = 'high_priority' in condition

    # Simulate each mind unit processing in "parallel"
    print(f"Simulating {num_minds} mind units processing...")
    for i in range(num_minds):
        mind_time, was_distracted = simulate_mind_unit_processing(
            is_distraction_condition, is_high_priority
        )
        individual_mind_times.append(mind_time)
        if was_distracted:
            distracted_minds_count += 1
        # print(f"  Mind Unit {i+1}: {mind_time:.2f}s {'(Distracted)' if was_distracted else ''}") # Verbose
        time.sleep(0.05) # Tiny pause to simulate thinking time in output

    # --- Hive Mind Response Rule: Consensus ---
    # The time taken for the *entire* hive to respond is the time the *last* unit finishes.
    hive_response_time = max(individual_mind_times)

    print(f"\nIndividual Mind Times (simulated): {[f'{t:.2f}s' for t in individual_mind_times]}")
    print(f"Number of units distracted: {distracted_minds_count}/{num_minds}")
    print(f"Hive Mind Response Time (Consensus): {hive_response_time:.2f} seconds.")
    print("-" * 50)
    time.sleep(1) # Pause between trials

    # We assume the hive eventually gets the *correct* answer if all units process;
    # the focus here is on the *time* cost imposed by conditions.
    # We return the collective time and the list of individual times for potential analysis.
    return hive_response_time, individual_mind_times, distracted_minds_count

# --- Main Experiment Loop ---

# Define the conditions to test
conditions = [
    'control',                   # No distractions, standard command implied
    'distraction_standard',      # Distractions active, standard command
    'distraction_high_priority'  # Distractions active, high-priority command (mitigates distraction)
]

results = {condition: [] for condition in conditions}

for condition in conditions:
    print(f"\n===== Starting Condition: {condition.upper()} =====")
    # input(f"Press Enter to begin the {condition} trials...") # Optional pause

    trial_collective_times = []
    trial_distraction_counts = []
    trial_time_variances = []

    for i in range(NUM_TRIALS_PER_CONDITION):
        print(f"\n--- Trial {i+1} of {NUM_TRIALS_PER_CONDITION} ({condition}) ---")
        collective_time, individual_times, distracted_count = run_hive_trial(condition, NUM_MINDS)

        trial_collective_times.append(collective_time)
        trial_distraction_counts.append(distracted_count)
        if len(individual_times) > 1:
            trial_time_variances.append(statistics.variance(individual_times))
        else:
            trial_time_variances.append(0)

    # Store aggregated results for the condition
    results[condition] = {
        'collective_times': trial_collective_times,
        'avg_collective_time': statistics.mean(trial_collective_times) if trial_collective_times else 0,
        'stdev_collective_time': statistics.stdev(trial_collective_times) if len(trial_collective_times) > 1 else 0,
        'avg_distracted_count': statistics.mean(trial_distraction_counts) if trial_distraction_counts else 0,
        'avg_time_variance': statistics.mean(trial_time_variances) if trial_time_variances else 0,
    }

# --- Basic Results Analysis ---

print("\n\n" + "="*20 + " Experiment Results " + "="*20)

for condition, data in results.items():
    print(f"\nCondition: {condition.upper()}")
    if not data or not data['collective_times']:
        print("  No data collected.")
        continue

    print(f"  Avg. Hive Response Time (Consensus): {data['avg_collective_time']:.2f}s (StdDev: {data['stdev_collective_time']:.2f}s)")
    print(f"  Avg. Distracted Units per Trial:   {data['avg_distracted_count']:.1f}/{NUM_MINDS}")
    print(f"  Avg. Variance in Unit Times:      {data['avg_time_variance']:.2f}")


# --- Interpretation ---
print("\n" + "="*20 + " Interpretation " + "="*20)
try:
    control_time = results['control']['avg_collective_time']
    distraction_std_time = results['distraction_standard']['avg_collective_time']
    distraction_hp_time = results['distraction_high_priority']['avg_collective_time']
    distraction_std_var = results['distraction_standard']['avg_time_variance']
    distraction_hp_var = results['distraction_high_priority']['avg_time_variance']


    print(f"\nImpact of Distraction (Standard Command):")
    print(f"  - Compared to control ({control_time:.2f}s), standard distractions increased avg. time to {distraction_std_time:.2f}s.")
    increase_pct = ((distraction_std_time / control_time) - 1) * 100 if control_time else 0
    print(f"  - Increase of {increase_pct:.1f}%")

    print(f"\nImpact of High-Priority Command (under Distraction):")
    print(f"  - Compared to standard distraction ({distraction_std_time:.2f}s), high-priority command reduced avg. time to {distraction_hp_time:.2f}s.")
    mitigation_pct = 100 - ((distraction_hp_time - control_time) / (distraction_std_time - control_time) * 100) if (distraction_std_time - control_time) != 0 else 0
    print(f"  - High-priority command mitigated the distraction effect by approx. {mitigation_pct:.1f}%.")

    print("\nCoordination (Variance):")
    print(f"  - Variance in unit times under standard distraction: {distraction_std_var:.2f}")
    print(f"  - Variance under high-priority distraction: {distraction_hp_var:.2f}")
    if distraction_hp_var < distraction_std_var:
         print("  - High-priority command appeared to improve coordination (lower variance).")
    else:
         print("  - High-priority command did not appear to reduce variance among units.")


except KeyError as e:
    print(f"\nCould not perform full comparison - missing data for condition: {e}")
except ZeroDivisionError:
     print("\nCould not perform full comparison due to division by zero (e.g., control time was zero).")
