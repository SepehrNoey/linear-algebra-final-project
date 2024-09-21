# Linear Algebra Final Project

This project is divided into two parts, both showcasing applications of linear algebra in solving real-world problems.

## Part 1: Lights Out Puzzle

### Description
The Lights Out puzzle is a grid-based game where each cell can either be "on" (1) or "off" (0). The goal is to turn all the lights off by toggling cells. Toggling a cell also toggles its adjacent neighbors. Using linear algebra techniques such as row reduction, this program finds the solution by determining the order of cells that need to be clicked to turn off all the lights. If no solution exists, it reports that as well.

### Demo
<video src="https://github.com/user-attachments/assets/b4e4a57d-3d56-4f42-99d9-2805a2c8f21c">
<video src="https://github.com/user-attachments/assets/d9c0181e-ae44-4c29-a7ee-a666aba16ce8">


### How to Use
1. In the `part1` directory, open `main.py`.
2. Define the game board as a numpy array in the `cells` variable. (Note: '1' represents a light that is on, and '0' represents a light that is off. The board must be square.)
3. Run `main.py`, and the solution (if it exists) will be printed in the console. You can verify the result using the game GUI.

## Part 2: Histogram Matching

### Description
Histogram matching involves transforming the distribution of pixel intensities in a source image to match those of a reference image. This technique can be useful for image processing tasks where the appearance of two images needs to be aligned.

### Demo
|Input Image|Reference Image|Matched Image|
|-----|-----|-----|
|![Source](https://github.com/user-attachments/assets/7d4938a5-ffe2-45e6-a976-8007a28a06a9)| ![Reference](https://github.com/user-attachments/assets/781b74a6-bd54-40cb-b7dd-111ac20abefa)|![matched_img](https://github.com/user-attachments/assets/91edf978-1a55-4829-a478-597d6264d81b)|

### How to Use
1. In the `part2` directory:
    - Place your "Reference image" in a file named `Reference.jpg`.
    - Place your "Source image" in a file named `Source.jpg`.
2. Run `runnable.py`, and the matched image will be created in the same directory as `matched_img.jpg`.



