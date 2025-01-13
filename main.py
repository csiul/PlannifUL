import requests
from bs4 import BeautifulSoup
from datetime import datetime
import argparse
import re

capsule_horraire_url = "https://capsuleweb.ulaval.ca/pls/etpr/bwckschd.p_get_crse_unsec"

def fetch_course_data(url, year, semester, department):
    data = [
        ("term_in", str(year) + str(semester).zfill(2)),
        ("sel_subj", "dummy"),
        ("sel_subj", department),
        ("sel_day", "dummy"),
        ("sel_schd", "dummy"),
        ("sel_schd", "%"),
        ("sel_insm", "dummy"),
        ("sel_camp", "dummy"),
        ("sel_camp", "%"),
        ("sel_levl", "dummy"),
        ("sel_levl", "%"),
        ("sel_sess", "dummy"),
        ("sel_sess", "%"),
        ("sel_instr", "dummy"),
        ("sel_instr", "%"),
        ("sel_ptrm", "dummy"),
        ("sel_ptrm", "%"),
        ("sel_attr", "dummy"),
        ("sel_attr", "%"),
        ("sel_crse", ""),
        ("sel_title", ""),
        ("sel_from_cred", ""),
        ("sel_to_cred", ""),
        ("begin_hh", "0"),
        ("begin_mi", "0"),
        ("begin_ap", "x"),
        ("end_hh", "0"),
        ("end_mi", "0"),
        ("end_ap", "x")
    ]
        
    response = requests.post(url, data=data)
    return response.text

def parse_course_schedules(html):
    soup = BeautifulSoup(html, 'html.parser')
    schedules = []

    course_titles = soup.find_all('th', {'class': 'ddtitle'})

    for course_title in course_titles:
        title_text = course_title.text.strip()
        schedule_table = course_title.find_next('table', {'class': 'datadisplaytable'})
        if schedule_table:
            rows = schedule_table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) > 1:
                    day_time = cells[1].text.strip()
                    day_week = cells[2].text.strip()
                    if day_time != 'ACU':
                        schedules.append((title_text, day_time, day_week))
    return schedules

def parse_time_range(time_range):
    start_time, end_time = time_range.split(' - ')
    return datetime.strptime(start_time, '%H:%M'), datetime.strptime(end_time, '%H:%M')

def time_ranges_overlap(range1, range2):
    start1, end1 = parse_time_range(range1)
    start2, end2 = parse_time_range(range2)
    return start1 < end2 and start2 < end1

def check_conflicts_with_slot(schedules, chosen_time, chosen_day):
    conflicts = []
    for schedule in schedules:
        if schedule[2] == chosen_day and time_ranges_overlap(schedule[1], chosen_time):
            conflicts.append(schedule)
    return conflicts

def validate_time_range(value):
    pattern = r"^\d{1,2}:\d{1,2} - \d{1,2}:\d{1,2}$"
    if not re.match(pattern, value):
        raise argparse.ArgumentTypeError(
            f"Invalid time range: '{value}'. Expected format is 'HH:MM - HH:MM'."
        )
    return value

def main():
    parser = argparse.ArgumentParser(
        description="Vérifiez si une plage horaire est en conflit avec des cours existants.",
        epilog="Exemple d'utilisation : python script.py -y 2025 -s 1 -d IFT GLO -t '18:00 - 21:00' -w L"
    )
    parser.add_argument("-y", "--year", type=int, required=True, help="Année du trimestre")
    parser.add_argument("-s", "--semester", type=int, choices=[1, 5, 9], required=True, help="Semestre ('1' pour Hiver, '5' pour Été, '9' pour Automne)")
    parser.add_argument("-d", "--departments", nargs='+' ,type=str, default=["IFT", "GLO"], help="Liste de département (par défaut : 'IFT' 'GLO')")
    parser.add_argument("-t", "--time", type=validate_time_range, required=True, help="Plage horaire choisie ('18:00 - 21:00')")
    parser.add_argument("-w", "--weekday", type=str, choices=["L", "M", "R", "J", "V"], required=True, help="Jour choisi ('L' pour Lundi, 'M' pour Mardi, 'R' pour Mercredi, 'J' pour Jeudi, 'V' pour Vendredi)")

    args = parser.parse_args()

    all_schedules = []

    for department in args.departments:
        html = fetch_course_data(capsule_horraire_url, args.year, args.semester, department)
        schedules = parse_course_schedules(html)
        all_schedules.extend(schedules)

    conflicts = check_conflicts_with_slot(all_schedules, args.time, args.weekday)

    for conflict in conflicts:
        print(f"Conflit avec {conflict[0]} à {conflict[1]}")

if __name__ == "__main__":
    main()