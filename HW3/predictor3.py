import gzip

# Function to read and process the trace file content into a list
def read_trace(file_name):
    trace = []
    with gzip.open(file_name, 'rt') as f:
        for line in f:
            addr, outcome = line.strip().split()
            trace.append((int(addr), outcome))
    return trace

# Constants representing the 2-bit predictor states
STRONGLY_TAKEN = 3
WEAKLY_TAKEN = 2
WEAKLY_NOT_TAKEN = 1
STRONGLY_NOT_TAKEN = 0

class BranchPredictor:
    def __init__(self, size=32, phr_length=4):
        # Initialize the predictor table with 32 entries, each containing a 2-bit counter
        self.size = size
        self.predictor_table = [WEAKLY_NOT_TAKEN] * size  # All entries are initialized as weakly not taken
        self.correct_predictions = 0  
        self.incorrect_predictions = 0  
        self.phr = 0  # Pattern history register
        self.phr_length = phr_length  # Length of the pattern history register, N

    def update_phr(self, outcome):
        # shift left, add new outcome, and mask with N bits (1 for 'T', 0 for 'N')
        self.phr = ((self.phr << 1) | (1 if outcome == 'T' else 0)) & ((1 << self.phr_length) - 1)

    def index(self, address):
        # XOR the branch instruction address with the PHR value to get the index
        return (address ^ self.phr) % self.size

    def predict(self, idx):
        # Return prediction based on the current 2-bit counter (0 or 1 -> predict N, 2 or 3 -> predict T)
        if self.predictor_table[idx] < WEAKLY_TAKEN:
            return 'N'  
        else:
            return 'T'  

    def update(self, address, actual_outcome):
        # Get the index for the address and predict outcome
        idx = self.index(address)
        prediction = self.predict(idx)

        # Check if the prediction was correct
        if prediction == actual_outcome:
            self.correct_predictions += 1
        else:
            self.incorrect_predictions += 1

        # Update the predictor table based on actual outcome
        if actual_outcome == 'T':
            if self.predictor_table[idx] < STRONGLY_TAKEN:  # Increment 2-bit counter
                self.predictor_table[idx] += 1
        else:
            if self.predictor_table[idx] > STRONGLY_NOT_TAKEN:  # Decrement 2-bit counter
                self.predictor_table[idx] -= 1

        # Update the PHR with the actual outcome
        self.update_phr(actual_outcome)

        return prediction

def simulate_branch_predictor(trace, history_length):
    # Create the predictor with the specified history length
    branch_predictor = BranchPredictor(phr_length=history_length)

    # Simulate the branch predictor
    for addr, outcome in trace:
        prediction = branch_predictor.update(addr, outcome)

    # Print results
    print(f"Accuracy (N = {history_length}):", branch_predictor.correct_predictions/
          (branch_predictor.correct_predictions+branch_predictor.incorrect_predictions)*100) 
    print("Correct Predictions:", branch_predictor.correct_predictions)
    print("Incorrect Predictions:", branch_predictor.incorrect_predictions) 

# Simulate the branch predictor with different N values
trace = read_trace('itrace.out.gz')
simulate_branch_predictor(trace, 2)
simulate_branch_predictor(trace, 4)
simulate_branch_predictor(trace, 8)
simulate_branch_predictor(trace, 16)
simulate_branch_predictor(trace, 32)