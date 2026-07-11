"""
Generate a synthetic dataset for the Student Career Path Recommendation System.
This script creates a balanced CSV dataset with realistic student profiles
mapped to appropriate career paths.
"""

import csv
import random
import os

# Career paths and their preferred skill/interest profiles
CAREER_PROFILES = {
    "Frontend Developer": {
        "math_range": (40, 85),
        "programming_range": (60, 95),
        "communication_range": (40, 80),
        "problem_solving_range": (50, 85),
        "web_interest_range": (7, 10),
        "mobile_interest_range": (3, 7),
        "ai_interest_range": (2, 6),
        "database_interest_range": (3, 6),
        "networking_interest_range": (1, 5),
        "cloud_interest_range": (2, 5),
        "design_interest_range": (6, 10),
        "preferred_subjects": ["Web Development", "Design", "Human-Computer Interaction"],
        "career_goals": ["Build beautiful websites", "Create interactive UIs", "Work at a tech startup"],
    },
    "Backend Developer": {
        "math_range": (55, 90),
        "programming_range": (65, 98),
        "communication_range": (35, 75),
        "problem_solving_range": (60, 95),
        "web_interest_range": (6, 10),
        "mobile_interest_range": (2, 6),
        "ai_interest_range": (3, 7),
        "database_interest_range": (5, 9),
        "networking_interest_range": (3, 7),
        "cloud_interest_range": (4, 8),
        "design_interest_range": (2, 6),
        "preferred_subjects": ["Data Structures", "Algorithms", "Database Systems"],
        "career_goals": ["Build scalable systems", "Work on server-side logic", "Become a software architect"],
    },
    "Full Stack Developer": {
        "math_range": (50, 90),
        "programming_range": (65, 98),
        "communication_range": (45, 85),
        "problem_solving_range": (55, 95),
        "web_interest_range": (7, 10),
        "mobile_interest_range": (4, 8),
        "ai_interest_range": (3, 7),
        "database_interest_range": (5, 9),
        "networking_interest_range": (3, 7),
        "cloud_interest_range": (4, 8),
        "design_interest_range": (4, 8),
        "preferred_subjects": ["Web Development", "Software Engineering", "Database Systems"],
        "career_goals": ["Build complete applications", "Work independently", "Lead development teams"],
    },
    "Mobile App Developer": {
        "math_range": (45, 85),
        "programming_range": (60, 95),
        "communication_range": (40, 80),
        "problem_solving_range": (50, 90),
        "web_interest_range": (3, 7),
        "mobile_interest_range": (8, 10),
        "ai_interest_range": (2, 6),
        "database_interest_range": (4, 8),
        "networking_interest_range": (2, 6),
        "cloud_interest_range": (3, 6),
        "design_interest_range": (5, 9),
        "preferred_subjects": ["Mobile Development", "UI Design", "Software Engineering"],
        "career_goals": ["Build mobile apps", "Work at a tech company", "Launch own app"],
    },
    "Data Analyst": {
        "math_range": (60, 95),
        "programming_range": (45, 85),
        "communication_range": (50, 90),
        "problem_solving_range": (55, 90),
        "web_interest_range": (2, 6),
        "mobile_interest_range": (1, 5),
        "ai_interest_range": (4, 8),
        "database_interest_range": (6, 10),
        "networking_interest_range": (1, 5),
        "cloud_interest_range": (2, 6),
        "design_interest_range": (3, 7),
        "preferred_subjects": ["Statistics", "Data Science", "Business Analytics"],
        "career_goals": ["Analyze data for insights", "Work in business intelligence", "Become a data scientist"],
    },
    "Machine Learning Engineer": {
        "math_range": (70, 100),
        "programming_range": (60, 98),
        "communication_range": (35, 75),
        "problem_solving_range": (70, 100),
        "web_interest_range": (2, 6),
        "mobile_interest_range": (1, 5),
        "ai_interest_range": (8, 10),
        "database_interest_range": (4, 8),
        "networking_interest_range": (2, 5),
        "cloud_interest_range": (4, 8),
        "design_interest_range": (1, 5),
        "preferred_subjects": ["Artificial Intelligence", "Machine Learning", "Deep Learning"],
        "career_goals": ["Build AI systems", "Research new algorithms", "Work at a research lab"],
    },
    "Cybersecurity Analyst": {
        "math_range": (50, 85),
        "programming_range": (50, 90),
        "communication_range": (40, 80),
        "problem_solving_range": (60, 95),
        "web_interest_range": (3, 7),
        "mobile_interest_range": (2, 6),
        "ai_interest_range": (2, 6),
        "database_interest_range": (3, 7),
        "networking_interest_range": (8, 10),
        "cloud_interest_range": (4, 8),
        "design_interest_range": (1, 5),
        "preferred_subjects": ["Network Security", "Ethical Hacking", "Cryptography"],
        "career_goals": ["Protect systems from attacks", "Work in security operations", "Become a security consultant"],
    },
    "Cloud/DevOps Engineer": {
        "math_range": (55, 90),
        "programming_range": (55, 90),
        "communication_range": (40, 80),
        "problem_solving_range": (55, 90),
        "web_interest_range": (4, 8),
        "mobile_interest_range": (2, 6),
        "ai_interest_range": (3, 7),
        "database_interest_range": (4, 8),
        "networking_interest_range": (6, 10),
        "cloud_interest_range": (8, 10),
        "design_interest_range": (1, 5),
        "preferred_subjects": ["Cloud Computing", "DevOps", "System Administration"],
        "career_goals": ["Manage cloud infrastructure", "Automate deployments", "Work at a cloud provider"],
    },
    "UI/UX Designer": {
        "math_range": (35, 75),
        "programming_range": (35, 70),
        "communication_range": (60, 100),
        "problem_solving_range": (45, 85),
        "web_interest_range": (5, 9),
        "mobile_interest_range": (4, 8),
        "ai_interest_range": (1, 5),
        "database_interest_range": (2, 5),
        "networking_interest_range": (1, 4),
        "cloud_interest_range": (1, 5),
        "design_interest_range": (8, 10),
        "preferred_subjects": ["Design", "Human-Computer Interaction", "Psychology"],
        "career_goals": ["Design user experiences", "Work at a design agency", "Become a product designer"],
    },
    "Database Administrator": {
        "math_range": (50, 85),
        "programming_range": (45, 80),
        "communication_range": (40, 75),
        "problem_solving_range": (55, 90),
        "web_interest_range": (3, 6),
        "mobile_interest_range": (1, 5),
        "ai_interest_range": (3, 7),
        "database_interest_range": (8, 10),
        "networking_interest_range": (4, 8),
        "cloud_interest_range": (5, 9),
        "design_interest_range": (1, 5),
        "preferred_subjects": ["Database Systems", "SQL", "Data Management"],
        "career_goals": ["Manage large databases", "Optimize database performance", "Work as a DBA"],
    },
}

DEPARTMENTS = [
    "Computer Science",
    "Information Technology",
    "Electronics",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Data Science",
    "Software Engineering",
]

CAREER_GOALS_MAP = {
    "Frontend Developer": "Build beautiful websites",
    "Backend Developer": "Build scalable systems",
    "Full Stack Developer": "Build complete applications",
    "Mobile App Developer": "Build mobile apps",
    "Data Analyst": "Analyze data for insights",
    "Machine Learning Engineer": "Build AI systems",
    "Cybersecurity Analyst": "Protect systems from attacks",
    "Cloud/DevOps Engineer": "Manage cloud infrastructure",
    "UI/UX Designer": "Design user experiences",
    "Database Administrator": "Manage large databases",
}


def random_in_range(range_tuple):
    """Return a random integer within the given range."""
    return random.randint(range_tuple[0], range_tuple[1])


def generate_student(career_path):
    """Generate a single student record for the given career path."""
    profile = CAREER_PROFILES[career_path]

    row = {
        "math_score": random_in_range(profile["math_range"]),
        "programming_score": random_in_range(profile["programming_range"]),
        "communication_score": random_in_range(profile["communication_range"]),
        "problem_solving_score": random_in_range(profile["problem_solving_range"]),
        "web_interest": random_in_range(profile["web_interest_range"]),
        "mobile_interest": random_in_range(profile["mobile_interest_range"]),
        "ai_interest": random_in_range(profile["ai_interest_range"]),
        "database_interest": random_in_range(profile["database_interest_range"]),
        "networking_interest": random_in_range(profile["networking_interest_range"]),
        "cloud_interest": random_in_range(profile["cloud_interest_range"]),
        "design_interest": random_in_range(profile["design_interest_range"]),
        "preferred_subject": random.choice(profile["preferred_subjects"]),
        "career_goal": random.choice(profile["career_goals"]),
        "recommended_path": career_path,
    }
    return row


def main():
    """Generate the synthetic dataset and save it to CSV."""
    random.seed(42)  # For reproducibility

    rows_per_career = 20  # 20 rows x 10 careers = 200 rows total
    all_rows = []

    for career_path in CAREER_PROFILES:
        for _ in range(rows_per_career):
            row = generate_student(career_path)
            all_rows.append(row)

    # Shuffle the rows so career paths are interleaved
    random.shuffle(all_rows)

    # Write to CSV
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "student_career_dataset.csv")

    fieldnames = [
        "math_score",
        "programming_score",
        "communication_score",
        "problem_solving_score",
        "web_interest",
        "mobile_interest",
        "ai_interest",
        "database_interest",
        "networking_interest",
        "cloud_interest",
        "design_interest",
        "preferred_subject",
        "career_goal",
        "recommended_path",
    ]

    with open(output_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Dataset generated successfully!")
    print(f"Total rows: {len(all_rows)}")
    print(f"Saved to: {output_path}")
    print(f"\nCareer path distribution:")

    from collections import Counter
    counts = Counter(row["recommended_path"] for row in all_rows)
    for career, count in sorted(counts.items()):
        print(f"  {career}: {count}")


if __name__ == "__main__":
    main()
