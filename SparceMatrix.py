import os

class SparseMatrix:
    """
    This class represents a sparse matrix. Sparse matrices store only the non-zero elements
    and their corresponding positions to save memory.
    """
    def __init__(self, numRows=None, numCols=None):
        """
        This function initializes a sparse matrix object.

        Args:
            numRows (int, optional): The number of rows in the matrix. Defaults to None.
            numCols (int, optional): The number of columns in the matrix. Defaults to None.
        """
        self.numRows = numRows
        self.numCols = numCols
        self.matrix = {}

    def loadFromMatrix(self, numRows, numCols, matrix):
        """
        This function loads a dense matrix (represented as a list of lists) into the sparse matrix object.

        Args:
            numRows (int): The number of rows in the matrix.
            numCols (int): The number of columns in the matrix.
            matrix (list of lists): A dense representation of the matrix.
        """
        self.numRows = numRows
        self.numCols = numCols
        self.matrix = {}

        for i in range(numRows):
            for j in range(numCols):
                if matrix[i][j] != 0:
                    self.matrix[(i, j)] = matrix[i][j]

    def getElement(self, currRow, currCol):
        """
        This function retrieves the value of an element in the sparse matrix.

        Args:
            currRow (int): The row index of the element.
            currCol (int): The column index of the element.

        Returns:
            int: The value of the element at the specified position. If the element is zero, returns 0.
        """
        return self.matrix.get((currRow, currCol), 0)

    def setElement(self, currRow, currCol, value):
        """
        This function sets the value of an element in the sparse matrix.

        Args:
            currRow (int): The row index of the element.
            currCol (int): The column index of the element.
            value (int): The value to set at the specified position.
        """
        if value != 0:
            self.matrix[(currRow, currCol)] = value
        elif (currRow, currCol) in self.matrix:
            del self.matrix[(currRow, currCol)]

    def add(self, other):
        """
        This function adds two sparse matrices and returns the resulting sparse matrix.

        Args:
            other (SparseMatrix): The other sparse matrix to add.

        Returns:
            SparseMatrix: The resulting sparse matrix after addition.
        """
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)

        # Merge self and other matrices
        for (row, col), value in self.matrix.items():
            result.setElement(row, col, value)

        for (row, col), value in other.matrix.items():
            result.setElement(row, col, result.getElement(row, col) + value)

        return self.removeZerosFromResult(result)


    def multiply(self, other):
        """
        This function multiplies two sparse matrices and returns the resulting sparse matrix.

        Args:
            other (SparseMatrix): The other sparse matrix to multiply with.

        Returns:
            SparseMatrix: The resulting sparse matrix after multiplication.
        """
        result = SparseMatrix(numRows=self.numRows, numCols=other.numCols)

        for (row1, col1), value1 in self.matrix.items():
            for (row2, col2), value2 in other.matrix.items():
                if col1 == row2:
                    result.setElement(row1, col2, result.getElement(row1, col2) + value1 * value2)

        return self.removeZerosFromResult(result)

    def subtract(self, other):
        """
        This function subtracts a sparse matrix from the current sparse matrix and returns the resulting sparse matrix.

        Args:
            other (SparseMatrix): The sparse matrix to subtract from the current matrix.

        Returns:
            SparseMatrix: The resulting sparse matrix after subtraction.
        """
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)

        # Merge self and other matrices
        for (row, col), value in self.matrix.items():
            result.setElement(row, col, value)

        for (row, col), value in other.matrix.items():
            result.setElement(row, col, result.getElement(row, col) - value)

        return self.removeZerosFromResult(result)

    def removeZerosFromResult(self, result):
        """
        This function removes zero elements from a sparse matrix.

        Args:
            result (SparseMatrix): The sparse matrix to remove zeros from.

        Returns:
            SparseMatrix: The sparse matrix with zeros removed.
        """
        for (row, col), value in list(result.matrix.items()):
            if value == 0:
                del result.matrix[(row, col)]
        
        return result

def isEqual(numRows1, numRows2, numCols1, numCols2, direction):
    """
    This function compares the dimensions of two matrices and checks for equality based on a given direction.

    Args:
        numRows1 (int): The number of rows in the first matrix.
        numCols1 (int): The number of columns in the first matrix.
        numRows2 (int): The number of rows in the second matrix.
        numCols2 (int): The number of columns in the second matrix.
        direction (str): The direction to compare equality. Can be "same" or "inverse".

    Returns:
        bool: True if the dimensions are equal according to the specified direction, False otherwise.
    """
    if (direction == 'same'):
        """
        Checks if both matrices have the same dimensions (rows and columns)
        """
        if (numRows1 == numRows2 and numCols1==numCols2):
            return True
    elif (direction == 'inverse'):
        """
        Checks if the number of rows in matrix 1 is equal to the number of columns in matrix 2,
        and vice versa (for matrix multiplication compatibility)
        """
        if (numRows1 == numCols2 and numCols1==numRows2):
            return True
    return False

def main():
    """
    This function is the entry point of the program. It allows users to perform addition, subtraction, and multiplication operations on sparse matrices.
    """
    print("Sparse Matrix Operations")

    matrixFile1 = input("Enter file path for first matrix: ")
    numRows1, numCols1, matrix1 = loadMatrixFromFile(matrixFile1)

    matrixFile2 = input("Enter file path for second matrix: ")
    numRows2, numCols2, matrix2 = loadMatrixFromFile(matrixFile2)

    matrix1Obj = SparseMatrix()
    matrix1Obj.loadFromMatrix(numRows1, numCols1, matrix1)

    matrix2Obj = SparseMatrix()
    matrix2Obj.loadFromMatrix(numRows2, numCols2, matrix2)

    result_folder = 'results'
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    while True:
        print("\nChoose an operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("")
        print("0. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            if not isEqual(numRows1, numRows2, numCols1, numCols2, 'same'):
                print('Can not perform addition to different matrices')
            else:    
                result = matrix1Obj.add(matrix2Obj)
                resultFileName = f"{os.path.splitext(os.path.basename(matrixFile1))[0]}_add_{os.path.splitext(os.path.basename(matrixFile2))[0]}.txt"
                saveMatrixToFile(result, os.path.join(result_folder, resultFileName))
                print(f"Addition result written to {resultFileName}")
        elif choice == '2':
            if not isEqual(numRows1, numRows2, numCols1, numCols2, 'same'):
                print('Can not perform substraction to different matrices')
            else:   
                result = matrix1Obj.subtract(matrix2Obj)
                resultFileName = f"{os.path.splitext(os.path.basename(matrixFile1))[0]}_subtract_{os.path.splitext(os.path.basename(matrixFile2))[0]}.txt"
                saveMatrixToFile(result, os.path.join(result_folder, resultFileName))
                print(f"Subtraction result written to {resultFileName}")
        elif choice == '3':
            if not isEqual(numRows1, numRows2, numCols1, numCols2, 'inverse'):
                print('Can not perform multiplication to different matrices')
            else:   
                result = matrix1Obj.multiply(matrix2Obj)
                resultFileName = f"{os.path.splitext(os.path.basename(matrixFile1))[0]}_multiply_{os.path.splitext(os.path.basename(matrixFile2))[0]}.txt"
                saveMatrixToFile(result, os.path.join(result_folder, resultFileName))
                print(f"Multiplication result written to {resultFileName}")
        elif choice == '0':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


def loadMatrixFromFile(matrixFilePath):
    """
    This function reads a sparse matrix representation from a text file and returns the number of rows, columns, and the matrix data.

    Args:
        matrixFilePath (str): The path to the text file containing the sparse matrix representation.

    Returns:
        tuple: A tuple containing three elements -
            - numRows (int): The number of rows in the matrix.
            - numCols (int): The number of columns in the matrix.
            - matrix (list of lists): A 2D list representing the sparse matrix, where non-zero elements are stored.

    Raises:
        ValueError: If the file cannot be opened or the format is invalid.
    """
    lines = []
    with open(matrixFilePath, 'r') as file:
        for line in file:
            lines.append(line.strip())

    # Remove whitespace and extract matrix dimensions
    lines = [line for line in lines if line.strip()]
    numRows = int(lines[0].split('=')[1])
    numCols = int(lines[1].split('=')[1])

    # Initialize matrix with zeros
    matrix = [[0 for _ in range(numCols)] for _ in range(numRows)]

    # Parse non-zero elements
    for line in lines[2:]:
        parts = line.strip('()').split(',')
        row = int(parts[0])
        col = int(parts[1])
        value = int(parts[2])

        if row < numRows and col < numCols:
            matrix[row][col] = value

        

    return numRows, numCols, matrix

    lines = []
    with open(matrixFilePath, 'r') as file:
        for line in file:
            lines.append(line.strip())

    # Remove whitespace and extract matrix dimensions
    lines = [line for line in lines if line.strip()]
    numRows = int(lines[0].split('=')[1])
    numCols = int(lines[1].split('=')[1])

    # Initialize matrix with zeros
    matrix = [[0 for _ in range(numCols)] for _ in range(numRows)]

    # Parse non-zero elements
    for line in lines[2:]:
        parts = line.strip('()').split(',')
        row = int(parts[0])
        col = int(parts[1])
        value = int(parts[2])
        print(len(matrix))
        print(f"{row} {col} {value}")
        matrix[row][col] = value

    return numRows, numCols, matrix

    lines = []
    with open(matrixFilePath, 'r') as file:
        for line in file:
            lines.append(line.strip())

    # Remove whitespace and extract matrix dimensions
    lines = [line for line in lines if line.strip()]
    numRows = int(lines[0].split('=')[1])
    numCols = int(lines[1].split('=')[1])

    # Initialize matrix with zeros
    matrix = [[0 for _ in range(numCols)] for _ in range(numRows)]

    # Parse non-zero elements
    for line in lines[2:]:
        parts = line.strip('()').split(',')
        row = int(parts[0])
        col = int(parts[1])
        value = int(parts[2])
        matrix[row][col] = value

    return numRows, numCols, matrix

def saveMatrixToFile(matrix, filePath):
    """
    This function saves a sparse matrix object to a text file in the specified format.

    Args:
        matrix (SparseMatrix): The sparse matrix object to save.
        filePath (str): The path to the output file.
    """
    with open(filePath, 'w') as file:
        for (row, col), value in matrix.matrix.items():
            file.write(f"({row}, {col}, {value})\n")


if __name__ == "__main__":
    main()
