def save_to_file(file_name, jobs):
    file = open(file_name, mode="w", encoding="utf-8", newline="")
    file.write("Title,Company,Description,Link\n")

    for job in jobs:
        file.write(f"{job['title']},{job['company']},{job['description']},{job['link']}\n")