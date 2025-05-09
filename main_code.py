import csv


def parse_lookup_table(filename):
    lookup = {}
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                dstport = int(row["dstport"])
                protocol = row["protocol"].strip().lower()
                tag = row["tag"].strip()
                lookup[(dstport, protocol)] = tag
            except (ValueError, KeyError) as e:
                print(f"Malformed Row at Lookup Table: {row} | Error: {e}")

    return lookup


def parse_log_file(filename, lookup, protocol_dict):
    tag_matches = {}
    port_protocol_matches = {}
    with open(filename, 'r') as f:
        for lineno, line in enumerate(f, 1):
            cleared_line = line.strip()
            if not cleared_line: # It means its blank line
                continue
            cleared_line = cleared_line.lower()
            splitted_line = cleared_line.split()
            if len(splitted_line) != 14:
                print(f"Malformed Log Data at Line {lineno}")
                continue
            
            protocol = int(splitted_line[7])
            if protocol not in protocol_dict:
                print(f"Invalid Protocol at Line {lineno}")
                continue
            
            protocol_name = protocol_dict[protocol]
            dstport = int(splitted_line[6])
            #print(dstport, protocol_name)
            tag = "Untagged"
            if (dstport, protocol_name) in lookup:
                tag = lookup[(dstport, protocol_name)]
            tag_matches[tag] = tag_matches.get(tag, 0) + 1
            
            #print(tag_matches[tag], tag)
            port_protocol_matches[(dstport, protocol_name)] = port_protocol_matches.get((dstport, protocol_name), 0) + 1
            #print(port_protocol_matches[dstport, protocol_name])
    return (tag_matches, port_protocol_matches)

def write_tag_counts_to_csv(tag_counts, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Tag', 'Count']) 
        for tag, count in tag_counts.items():
            writer.writerow([tag, count])

def write_port_protocol_matches_to_csv(port_protocol_matches, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Port', 'Protocol', 'Count']) 
        for (port, protocol), count in port_protocol_matches.items():
            writer.writerow([port, protocol, count])



def parse_protocol_table(filename):
    protocol_dict = {}
    with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    decimal = int(row['Decimal'])
                    keyword = row['Keyword'].strip().lower()
                    protocol_dict[decimal] = keyword.strip().lower()
                except (ValueError, KeyError) as e:
                    print(f"Malformed Row at Protocol Table: {row} | Error: {e}")
    return protocol_dict



def log_analyzer(protocol_table_filename, lookup_table_filename, log_filename, tag_counts_filename, port_protocol_filename):    
    protocol_dict = parse_protocol_table(protocol_table_filename)
    lookup = parse_lookup_table(lookup_table_filename)
    pair = parse_log_file(log_filename, lookup, protocol_dict)
    write_tag_counts_to_csv(pair[0], tag_counts_filename)
    write_port_protocol_matches_to_csv(pair[1], port_protocol_filename)



log_analyzer("protocol-numbers-1.csv", "lookup.csv", "log.txt", "tag_counts.csv", "port_protocol.csv")

