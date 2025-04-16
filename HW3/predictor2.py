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
    def __init__(self, size=32):
        # Initialize the predictor table with 32 entries, each containing a 2-bit counter
        self.size = size
        self.predictor_table = [WEAKLY_NOT_TAKEN] * size # All entries are initialized as weakly not taken
        self.correct_predictions = 0  
        self.incorrect_predictions = 0  

    def index(self, address):
        # Use modulo to limit the address within the range of the predictor table size
        return address % self.size

    def predict(self, idx):
        # Return prediction based on the current 2-bit counter (0 or 1 -> predict N, 2 or 3 -> predict T)
        if self.predictor_table[idx] < WEAKLY_TAKEN:
            return 'N'  # Predict Not Taken
        else:
            return 'T'  # Predict Taken

    def update(self, address, actual_outcome):
        # Get the index for the address
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
        else:  # Outcome is 'N'
            if self.predictor_table[idx] > STRONGLY_NOT_TAKEN:  # Decrement 2-bit counter
                self.predictor_table[idx] -= 1

        return prediction, actual_outcome

def simulate_branch_predictor(trace_file):
    trace = read_trace(trace_file)

    # Create the predictor
    branch_predictor = BranchPredictor()

    # Simulate the branch predictor
    for addr, outcome in trace:
        prediction, actual = branch_predictor.update(addr, outcome)

    # Print the results
    print("\nCorrect Predictions:", branch_predictor.correct_predictions)
    print("Incorrect Predictions:", branch_predictor.incorrect_predictions)
    print("Accuracy:", branch_predictor.correct_predictions/
          (branch_predictor.correct_predictions+branch_predictor.incorrect_predictions)*100)    
    # print("\nPredictor Table:", branch_predictor.predictor_table)

# Run the simulation
simulate_branch_predictor('itrace.out.gz')
