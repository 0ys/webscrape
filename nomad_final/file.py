import csv

def save_to_file(name, jobs_db):
    file = open(name, mode="w", encoding="utf-8", newline="")
    writer = csv.writer(file)
    writer.writerow(["Title", "Company", "Location", "Link"])

    for job in jobs_db:
        writer.writerow(job.values())
    file.close()