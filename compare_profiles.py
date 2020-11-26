import sys

def compare_profiles(prof1, prof2):
	n_matches = 0
	for i in range(0, len(prof1)):
		if prof1[i] == prof2[i] or prof1[i] == '-' or prof2[i] == '-':
			n_matches += 1

	return float(n_matches) / len(prof1)
	

f_query = sys.argv[1]
f_db = sys.argv[2]
match_threshold = float(sys.argv[3])

with open(f_query) as f1:
	queries = f1.readlines()

with open(f_db) as f2:
	db = f2.readlines()

query_loci = queries[0].split()[1:]
db_loci = db[0].split()[1:]

if query_loci == db_loci:
	print('CHECK: query and db loci match.')
else:
	print('ERROR: query and db have different loci. exiting.')
	exit()


queries_size = len(queries[1:])
db_size = len(db[1:])

print('Comparing {} profiles in {} with {} profiles in {}'.format(queries_size, f_query, db_size, f_db))

for nq, query in enumerate(queries[1:]):
	query_id = query.split()[0]
	query_profile = query.split()[1:]
	query_profile_size = len(query_profile)
	print('Looking for profile {} (analyzed queries: {:.2f}%)'.format(query_id, float(nq)/queries_size*100))

	for db_entry in db[1:]:
		db_id = db_entry.split()[0]
		db_profile = db_entry.split()[1:]
		db_profile_size = len(db_profile)
		if query_profile_size != db_profile_size:
			print('ERROR: Database profile {} (size = {}) and query profile {} (size = {}) have different size. Skipping it.'
				.format(db_id, db_profile_size, query_id, query_profile_size))
			continue

		match_value = compare_profiles(query_profile, db_profile)
		if match_value >= match_threshold:
			print('FOUND MATCH: Database profile {} matches with query profile {} (matching value = {:.2f}%)'.format(db_id, query_id, 100*match_value))

