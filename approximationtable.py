import sys

# sbox from the tutorial
#sbox = [0xe, 4, 0xd, 1, 2, 0xf, 0xb, 8, 3, 0xa, 6, 0xc, 5, 9, 0, 7]
# sbox = [0xf, 3, 0xa, 6, 4, 1, 0xb, 9, 0xe, 5, 0, 0xd, 2, 0xc, 7, 8]

s_box = [2, 0xc, 4, 1, 7, 0xa, 0xb, 6, 8, 5, 3, 0xf, 0xd, 0, 0xe, 9]
SIZE_SBOX = len(s_box)

# compute the linear approximation for a given "input = output" equation
def linearApprox(input_int, output_int):
    total = 0
    # range over the input
    for i in range(SIZE_SBOX):
        # get input and output of our equations
        input_masked = i & input_int
        output_masked = s_box[i] & output_int
        # same result?
        if (bin(input_masked).count("1") - bin(output_masked).count("1")) % 2 == 0:
            total += 1 
    # get the number of results compared to 8/16
    result = total - (SIZE_SBOX//2)
    if result > 0:
        result = "+" + str(result)
    else:
        result = str(result)

    return result

def main():
    # print table
    # rows
    sys.stdout.write( "    | ")
    for i in range(SIZE_SBOX):
        sys.stdout.write(hex(i)[2:].rjust(3) + " ")

    print("")

    print(" " + "-" * (SIZE_SBOX * 4 + 4))

    for row in range(SIZE_SBOX):
        sys.stdout.write(hex(row)[2:].rjust(3) +  " | ")
        # cols
        for col in range(SIZE_SBOX):
            # print the linear approx
            sys.stdout.write( linearApprox(row, col).rjust(3) + " ")

        print("")

if __name__ == "__main__":
    main()