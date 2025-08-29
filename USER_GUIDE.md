# Sorting Algorithm Visualizer - User Guide

## 🚀 Getting Started

1. **Launch the Application**
   ```bash
   cd Documents\Projects\Algorithm_visualizer
   python main.py
   ```

2. **Application Layout**
   The application has three main panels:
   - **Left Panel**: Controls (algorithm selection, buttons, settings)
   - **Center Panel**: Visualization canvas with animated bars
   - **Right Panel**: Color legend and completion messages

## 📋 How to Use

### Step 1: Select an Algorithm
- Click the **Algorithm dropdown** in the left panel
- Choose from: Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, or Quick Sort
- You'll see the algorithm's time/space complexity and description appear below

### Step 2: Set Your Data
**Option A: Use Random Data (Recommended for first use)**
- Use the **Array Size slider** to choose size (10-50 elements)
- Click **"Generate Random"** button
- Random numbers will appear in the custom input field

**Option B: Enter Custom Data**
- Type numbers in the **Custom Input** field
- Format: `5,3,8,1,9` (comma-separated, numbers 1-100)
- Click **"Apply"** button
- Maximum 50 elements allowed

### Step 3: Start the Animation
- Click the **Play button (▶)** 
- Watch the bars animate with colors:
  - **Blue**: Unsorted elements
  - **Orange**: Elements being compared
  - **Red**: Elements being swapped
  - **Green**: Sorted elements (final position)

### Step 4: Control the Animation
- **Pause (⏸)**: Pause animation (can resume)
- **Reset (⟲)**: Return to original unsorted state
- **Speed Slider**: Adjust speed from 0.5x to 3.0x (works in real-time)

## 🎯 Tips for Best Learning Experience

### For Beginners
1. **Start with small arrays** (10-15 elements) to see details clearly
2. **Begin with Bubble Sort** - easiest to understand
3. **Use slow speed** (0.5x-1.0x) initially
4. **Watch the step counter** and operation descriptions

### For Advanced Users
1. **Compare algorithms** by running the same data through different algorithms
2. **Use larger arrays** (40-50 elements) to see performance differences
3. **Try worst-case scenarios**:
   - Reverse sorted: `50,49,48,47,46,...,3,2,1`
   - Nearly sorted: `1,2,3,4,6,5,7,8,9,10`

### Understanding Different Algorithms

**Bubble Sort** (`O(n²)`)
- Watch adjacent comparisons
- Notice how largest elements "bubble" to the end
- Good for understanding basic sorting concept

**Selection Sort** (`O(n²)`)
- Observe how it finds the minimum each pass
- Notice the sorted portion growing from left
- Very predictable number of comparisons

**Insertion Sort** (`O(n²)`)
- See how elements are inserted into sorted portion
- Works like sorting playing cards
- Efficient for small or nearly sorted arrays

**Merge Sort** (`O(n log n)`)
- Watch the divide-and-conquer approach
- Notice the merging of sorted subarrays
- Consistent performance regardless of input

**Quick Sort** (`O(n log n)`)
- Observe pivot selection and partitioning
- See how elements are arranged around the pivot
- Very efficient for random data

## 🔧 Troubleshooting

### Problem: "Nothing happens when I click Play"
**Solution**: Make sure you've selected an algorithm from the dropdown first

### Problem: "Custom input not accepted"
**Solution**: Check that your input follows the format:
- Numbers between 1-100
- Comma-separated: `5,3,8,1,9`
- Maximum 50 elements
- No letters or special characters

### Problem: "Animation too fast/slow"
**Solution**: Use the speed slider (bottom left) to adjust in real-time

### Problem: "Can't see all the bars"
**Solution**: Try a smaller array size (use the Array Size slider)

## 📚 Educational Features

### Real-time Information
- **Step Counter**: Shows current step / total steps
- **Operation Description**: Explains what's happening each step
- **Algorithm Info**: Time and space complexity, description
- **Progress Tracking**: Visual progress indicator

### Completion Statistics
- Total steps taken
- Time elapsed
- Final "Sort Complete!" celebration

## 🎨 Visual Cues

| Color | Meaning | When You See It |
|-------|---------|----------------|
| **Blue** | Unsorted | Initial state, untouched elements |
| **Orange** | Comparing | Algorithm is comparing these elements |
| **Red** | Swapping | Elements are being swapped |
| **Green** | Sorted | Element is in its final correct position |

## 📖 Sample Learning Sessions

### Session 1: Basic Understanding (15 minutes)
1. Array: `5,3,8,1,9`
2. Algorithm: Bubble Sort
3. Speed: 0.5x
4. Focus: Watch each comparison and swap

### Session 2: Algorithm Comparison (20 minutes)
1. Same array: `10,9,8,7,6,5,4,3,2,1`
2. Run each algorithm with this reverse-sorted data
3. Speed: 1.0x
4. Compare step counts and patterns

### Session 3: Performance Analysis (25 minutes)
1. Large array: Use size 50 with random data
2. Try: Bubble vs Merge vs Quick Sort
3. Speed: 2.0x-3.0x
4. Observe efficiency differences

## 💡 Quick Reference

| Action | How To |
|--------|--------|
| Change algorithm | Click dropdown, select algorithm |
| New random data | Adjust size slider, click "Generate Random" |
| Enter custom data | Type in field, click "Apply" |
| Start animation | Click ▶ (Play) |
| Pause animation | Click ⏸ (Pause) |
| Reset to start | Click ⟲ (Reset) |
| Change speed | Move speed slider |
| View progress | Check step counter and description |

---

**Happy Learning!** 🎓 Use this visualizer to deepen your understanding of how different sorting algorithms work and perform.