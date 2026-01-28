from typing import List
from collections import deque
import math

class WeightedAverage:
    def __init__(self, w: List[float]):
        """
        Initialize the WeightedAverage filter with given weights.
        
        Args:
            w: List of weights for the weighted average calculation.
               The length of w determines the window size (n).
        """
        self.w = w
        self.n = len(w)
        
        # Use deque for efficient FIFO operations
        self.buffer = deque(maxlen=self.n)
        
        # Track the weighted sum for efficiency
        self.weighted_sum = 0.0
        
        # Fill buffer with zeros initially
        for _ in range(self.n):
            self.buffer.append(0.0)
    
    def process(self, x: float) -> float:
        """
        Process a new signal value and return the weighted average.
        
        Args:
            x: New signal value (current entry at index 0)
            
        Returns:
            Weighted average of the last n values
        """
        # Remove the oldest value from weighted sum
        oldest = self.buffer[0]
        self.weighted_sum -= self.w[0] * oldest
        
        # Shift weights in our calculation
        for i in range(self.n - 1):
            current_val = self.buffer[i + 1]
            self.weighted_sum -= self.w[i] * current_val
            self.weighted_sum += self.w[i + 1] * current_val
        
        # Add the new value with weight w[0]
        self.weighted_sum += self.w[0] * x
        
        # Update buffer: new value becomes position 0, shift others right
        # Convert deque to list for shifting
        buffer_list = list(self.buffer)
        
        # Shift elements to the right
        for i in range(self.n - 1, 0, -1):
            buffer_list[i] = buffer_list[i - 1]
        
        # Insert new value at position 0
        buffer_list[0] = x
        
        # Update deque
        self.buffer = deque(buffer_list, maxlen=self.n)
        
        # Calculate and return the weighted average
        if self.n > 0:
            return self.weighted_sum / self.n
        return 0.0
    
    def __str__(self):
        return f"WeightedAverage(window_size={self.n}, weights={self.w})"


def test_weighted_average():
    """Test the WeightedAverage class with the provided example."""
    print("=== Test 1: Example from problem ===")
    w = [5, 4, 3, 2, 1]
    x_values = [1, 2, 3, 4, 5]
    
    wa = WeightedAverage(w)
    
    print(f"Weights: {w}")
    print("Processing values:")
    
    # Process each value
    for i, x in enumerate(x_values):
        result = wa.process(x)
        print(f"  x={x}, buffer={list(wa.buffer)}, weighted_sum={wa.weighted_sum:.2f}, y={result:.2f}")
    
    print(f"\nFinal result: {result:.2f}")
    print(f"Expected: 7.0")
    print(f"Test {'PASSED' if abs(result - 7.0) < 0.0001 else 'FAILED'}")
    
    return wa


def test_moving_average():
    """Test with weights equal to 1 (simple moving average)."""
    print("\n=== Test 2: Moving Average (weights all 1) ===")
    
    # Create weights with all 1's for window size of 5
    w = [1, 1, 1, 1, 1]
    ma = WeightedAverage(w)
    
    # Test sequence
    test_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print("Window size: 5, all weights = 1")
    print("Values and their moving averages:")
    
    for i, x in enumerate(test_values):
        result = ma.process(x)
        buffer_list = list(ma.buffer)
        
        # Calculate expected manually for verification
        if i < 4:  # Buffer not full yet
            expected = sum(test_values[:i+1]) / (i+1)
        else:
            expected = sum(test_values[i-4:i+1]) / 5
        
        print(f"  x={x:2d}, buffer={[f'{v:.1f}' for v in buffer_list]}, "
              f"y={result:.2f}, expected={expected:.2f}")
        
        # Verify
        assert abs(result - expected) < 0.0001, f"Moving average mismatch at index {i}"
    
    print("Moving average test PASSED")
    
    return ma


def test_sine_wave():
    """Test with a sine wave signal as suggested in the problem."""
    print("\n=== Test 3: Sine Wave Test ===")
    
    # Parameters for sine wave
    frequency = 1.0  # Hz
    sampling_rate = 10  # samples per second
    duration = 2.0  # seconds
    
    # Generate sine wave
    num_samples = int(duration * sampling_rate)
    time_points = [i / sampling_rate for i in range(num_samples)]
    sine_wave = [math.sin(2 * math.pi * frequency * t) for t in time_points]
    
    # Test with window size of 5, all weights = 1 (moving average)
    window_size = 5
    w = [1] * window_size
    wa = WeightedAverage(w)
    
    print(f"Sine wave: frequency={frequency}Hz, sampling={sampling_rate}Hz, "
          f"duration={duration}s, window_size={window_size}")
    print("\nFirst 10 samples with their moving averages:")
    
    results = []
    for i in range(min(20, len(sine_wave))):  # Show first 20 samples
        x = sine_wave[i]
        result = wa.process(x)
        results.append(result)
        
        buffer_list = list(wa.buffer)
        print(f"  t={time_points[i]:.2f}s, x={x:.4f}, y={result:.4f}")
    
    print("\nSine wave test completed successfully")
    
    # Additional verification: sum of last 5 results
    if len(results) >= 10:
        print(f"\nSample verification (indices 5-9):")
        for i in range(5, 10):
            print(f"  Sample {i}: x={sine_wave[i]:.4f}, filtered={results[i]:.4f}")


def test_custom_scenario():
    """Test with custom weights and values."""
    print("\n=== Test 4: Custom Scenario ===")
    
    w = [3, 2, 1]  # Window size 3
    wa = WeightedAverage(w)
    
    test_values = [10, 20, 30, 40, 50]
    
    print(f"Weights: {w} (window size: {len(w)})")
    print("Processing values:")
    
    expected_results = []
    results = []
    
    for i, x in enumerate(test_values):
        result = wa.process(x)
        results.append(result)
        
        # Manual calculation for verification
        if i == 0:
            # Buffer: [10, 0, 0]
            expected = (3*10 + 2*0 + 1*0) / 3
        elif i == 1:
            # Buffer: [20, 10, 0]
            expected = (3*20 + 2*10 + 1*0) / 3
        elif i == 2:
            # Buffer: [30, 20, 10]
            expected = (3*30 + 2*20 + 1*10) / 3
        elif i == 3:
            # Buffer: [40, 30, 20]
            expected = (3*40 + 2*30 + 1*20) / 3
        else:  # i == 4
            # Buffer: [50, 40, 30]
            expected = (3*50 + 2*40 + 1*30) / 3
        
        expected_results.append(expected)
        
        buffer_list = list(wa.buffer)
        print(f"  x={x:2d}, buffer={[f'{v:.1f}' for v in buffer_list]}, "
              f"y={result:.2f}, expected={expected:.2f}")
        
        # Verify
        assert abs(result - expected) < 0.0001, f"Mismatch at index {i}"
    
    print("Custom scenario test PASSED")


def main():
    """Run all tests."""
    print("Weighted Sum Average Implementation Tests")
    print("=" * 50)
    
    # Run all tests
    test_weighted_average()
    test_moving_average()
    test_sine_wave()
    test_custom_scenario()
    
    print("\n" + "=" * 50)
    print("All tests completed successfully!")


if __name__ == "__main__":
    main()