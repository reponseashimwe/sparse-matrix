# Sparse Matrix Operations

This Python program implements operations on sparse matrices, including addition, subtraction, and multiplication. It reads sparse matrices from input files, performs the specified operation, and saves the result to an output file.

## Prerequisites

Before running the program, ensure you have Python installed on your system.

## Usage

1. Clone the repository or download the code files.
2. Open a terminal or command prompt.
3. Navigate to the directory containing the code files.
4. Run the program using the following command:

   ```
   python SparseMatrix.py
   ```

5. Follow the on-screen instructions to input the file paths for the matrices and choose the operation to perform.

## Input File Format

The input file format for sparse matrices should adhere to the following structure:

```
rows=<number_of_rows>
cols=<number_of_columns>
(row, col, value)
(row, col, value)
...
```

Where:

- `<number_of_rows>`: The number of rows in the matrix.
- `<number_of_columns>`: The number of columns in the matrix.
- `(row, col, value)`: Each line represents a non-zero element in the matrix, with the row index, column index, and value separated by commas.

Example:

```
rows=3
cols=3
(0, 1, 5)
(1, 0, 3)
(2, 2, 2)
```

## Output

The result of the matrix operation will be saved to a file in the `results` folder. The file name will indicate the operation performed and the names of the input matrices.

## Supported Operations

1. Addition
2. Subtraction
3. Multiplication

## Author

(Reponse Ashimwe)[https://github.com/reponseashimwe]
