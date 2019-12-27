
if __name__ == "__main__":
    infile_name = "infile.csv"
    outfile_basename = "infile"
    outfile_extension = ".csv"
    outfile_count = 0
    max_size = 10
    with open("infile.csv", 'r') as infile:
        infile_contents = infile.readlines()

    for i, line in enumerate(infile_contents):
        if i % max_size == 0:
            if outfile_count > 0:
                outfile.close()
            outfile_count += 1
            outfile = open(outfile_basename + str(outfile_count) + outfile_extension, "w")
        outfile.write(line)

    outfile.close()
