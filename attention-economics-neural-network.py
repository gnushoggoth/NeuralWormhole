import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

class AttentionEconomicsModel(nn.Module):
    """
    A neural network model that simulates the concept of attention economics
    through repeated exposure and learning stabilization.
    
    The model represents how repeated exposure (like listening to the same song)
    can lead to increased familiarity and optimization in neural networks.
    """
    def __init__(self, input_size=1, hidden_size=10):
        super().__init__()
        # Create layers that represent cognitive processing
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )
    
    def forward(self, x):
        """
        Forward pass simulating the 'stabilization' of attention 
        through repeated exposure.
        """
        return self.network(x)

def compare_attention_economics(repeat_count, song_length):
    """
    Enhanced version of the original function that demonstrates 
    attention economics through neural network learning.
    
    Args:
    - repeat_count (int): Number of times to repeat the 'stimulus'
    - song_length (float): Length of the 'stimulus'
    
    Returns:
    - str: Detailed analysis of attention economics
    """
    total_time = repeat_count * song_length
    
    # Simulate learning through repeated exposure
    model = AttentionEconomicsModel()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.MSELoss()
    
    # Track learning progression
    learning_progression = []
    
    # Simulate repeated exposure
    for epoch in range(repeat_count):
        # Generate a simple input representing the 'stimulus'
        input_data = torch.tensor([song_length], dtype=torch.float32)
        target = torch.tensor([song_length * 2], dtype=torch.float32)  # Example target
        
        # Forward pass
        prediction = model(input_data)
        
        # Calculate loss
        loss = loss_fn(prediction, target)
        learning_progression.append(loss.item())
        
        # Backward pass and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    # Visualize learning progression
    plt.figure(figsize=(10, 5))
    plt.plot(learning_progression, label='Loss Progression')
    plt.title('Attention Economics: Learning through Repetition')
    plt.xlabel('Repetition Count')
    plt.ylabel('Loss')
    plt.legend()
    plt.tight_layout()
    plt.savefig('attention_economics_learning.png')
    plt.close()
    
    # Detailed analysis
    analysis = (
        f"Attention Economics Simulation:\n"
        f"- Total Exposure Time: {total_time} minutes\n"
        f"- Repetition Count: {repeat_count}\n"
        f"- Initial Loss: {learning_progression[0]:.4f}\n"
        f"- Final Loss: {learning_progression[-1]:.4f}\n"
        f"- Loss Reduction: {(learning_progression[0] - learning_progression[-1]) / learning_progression[0] * 100:.2f}%\n"
        "\nAnalogy Explanation:\n"
        "Just as repeated listening helps stabilize cognitive comfort, "
        "neural networks optimize through repeated exposure, "
        "reducing loss and improving predictive accuracy."
    )
    
    return analysis

# Example usage
if __name__ == "__main__":
    result = compare_attention_economics(5, 3)
    print(result)
