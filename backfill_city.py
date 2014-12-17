cities_file = open('cities15000.txt', 'r')

read = 0
for line in cities_file:
    parts = line.split("\t")
    part_no = 1
    for part in parts:
        print "part " + str(part_no), part
        part_no = part_no + 1
    read = read + 1
    if read == 5:
        break
