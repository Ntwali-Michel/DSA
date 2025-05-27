class SparseMatrix:
    def __init__(self, filepath=None, rows=0, cols=0):
        self.rows = rows
        self.cols = cols
        self.data = {}  # {(row, col): value}
        if filepath:
            self._load_from_file(filepath)

    def _parse_line(self, line):
        line = line.strip()
        if not line:
            return None
        if line.startswith("rows="):
            return ("rows", int(line[5:].strip()))
        elif line.startswith("cols="):
            return ("cols", int(line[5:].strip()))
        elif line.startswith("(") and line.endswith(")"):
            try:
                parts = line[1:-1].split(',')
                r = int(parts[0].strip())
                c = int(parts[1].strip())
                v = int(parts[2].strip())
                return (r, c, v)
            except:
                raise ValueError("Input file has wrong format")
        else:
            raise ValueError("Input file has wrong format")

    def _load_from_file(self, filepath):
        with open(filepath, 'r') as f:
            for line in f:
                result = self._parse_line(line)
                if result is None:
                    continue
                if result[0] == "rows":
                    self.rows = result[1]
                elif result[0] == "cols":
                    self.cols = result[1]
                else:
                    r, c, v = result
                    self.set_element(r, c, v)

    def set_element(self, r, c, v):
        if r >= self.rows or c >= self.cols:
            raise IndexError("Element out of bounds")
        if v != 0:
            self.data[(r, c)] = v

    def get_element(self, r, c):
        return self.data.get((r, c), 0)

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match for addition")
        result = SparseMatrix(rows=self.rows, cols=self.cols)
        for key, val in self.data.items():
            result.data[key] = val
        for key, val in other.data.items():
            result.data[key] = result.data.get(key, 0) + val
        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match for subtraction")
        result = SparseMatrix(rows=self.rows, cols=self.cols)
        for key, val in self.data.items():
            result.data[key] = val
        for key, val in other.data.items():
            result.data[key] = result.data.get(key, 0) - val
        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions do not match for multiplication")
        result = SparseMatrix(rows=self.rows, cols=other.cols)
        for (i, k), val1 in self.data.items():
            for j in range(other.cols):
                val2 = other.get_element(k, j)
                if val2 != 0:
                    result.data[(i, j)] = result.data.get((i, j), 0) + val1 * val2
        return result

    def print_sample(self, n=10):
        print("Showing first few non-zero elements:")
        count = 0
        for (r, c), v in self.data.items():
            print(f"({r}, {c}, {v})")
            count += 1
            if count >= n:
                break

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            f.write(f"rows={self.rows}\n")
            f.write(f"cols={self.cols}\n")
            for (r, c), v in self.data.items():
                f.write(f"({r}, {c}, {v})\n")
        print(f"✅ Saved to {filename}")


def main():
    print("=== Sparse Matrix Calculator ===")
    file1 = input("Enter path to first matrix file: ").strip()
    file2 = input("Enter path to second matrix file: ").strip()

    try:
        A = SparseMatrix(file1)
        B = SparseMatrix(file2)

        print("\nChoose operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        choice = input("Your choice (1/2/3): ")

        if choice == "1":
            if A.rows != B.rows or A.cols != B.cols:
                print("❌ Addition not allowed: Matrix dimensions don't match.")
                return
            result = A.add(B)

        elif choice == "2":
            if A.rows != B.rows or A.cols != B.cols:
                print("❌ Subtraction not allowed: Matrix dimensions don't match.")
                return
            result = A.subtract(B)

        elif choice == "3":
            if A.cols != B.rows:
                print("❌ Multiplication not allowed: A.cols must equal B.rows.")
                return
            result = A.multiply(B)
        else:
            print("Invalid choice")
            return

        result.print_sample()

        save = input("Do you want to save the result to a file? (y/n): ").lower()
        if save == "y":
            result.save_to_file("result_matrix.txt")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
