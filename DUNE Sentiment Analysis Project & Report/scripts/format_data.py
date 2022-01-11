import csv

def main():
	with open("../data/Dune_sample_1000.csv", 'r') as ds:
		reader = csv.DictReader(ds)
		fieldnames = reader.fieldnames
		fieldnames.append("sentiment")
		fieldnames.append("topic")
		with open("../data/Dune_1000.csv", 'w') as o:
			writer = csv.DictWriter(o, fieldnames=fieldnames)
			writer.writeheader()
			for row in reader:
				row["sentiment"]=""
				row["topic"] = ""
				writer.writerow(row)


if __name__=="__main__":
	main()
