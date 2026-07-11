"""
Flask Web Application for Student Career Path Recommendation System.

Routes:
  GET  /        - Home page with student input form
  POST /predict - Process form and show ML prediction result
  GET  /about   - About page explaining the system
  GET  /health  - JSON health check endpoint
"""

import os
import joblib
import numpy as np
from flask import Flask, render_template, request, jsonify

# ---------------------------------------------------------------------------
# App initialization
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "student-career-recommender-secret-key"

# ---------------------------------------------------------------------------
# Paths to saved model artifacts
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "career_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")

# Load model and encoder at startup
model = None
label_encoder = None

try:
    model = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(ENCODER_PATH)
    print("Model and label encoder loaded successfully.")
except FileNotFoundError:
    print(
        "WARNING: Model files not found. "
        "Run train_model.py before starting the app."
    )

# ---------------------------------------------------------------------------
# Career path details - descriptions, skills, roadmaps, mini-projects
# ---------------------------------------------------------------------------
CAREER_DETAILS = {
    "Frontend Developer": {
        "description": (
            "A Frontend Developer builds the visual and interactive parts of "
            "websites and web applications. They focus on user experience, "
            "responsive design, and browser performance."
        ),
        "skills": [
            "HTML5, CSS3, JavaScript (ES6+)",
            "React.js or Angular",
            "Bootstrap / Tailwind CSS",
            "Responsive & mobile-first design",
            "Version control with Git",
            "Basic understanding of REST APIs",
        ],
        "roadmap": [
            "Learn HTML5 and CSS3 fundamentals",
            "Master JavaScript and DOM manipulation",
            "Learn Bootstrap for responsive layouts",
            "Pick up a framework like React or Angular",
            "Understand version control with Git/GitHub",
            "Build and deploy portfolio projects",
        ],
        "projects": [
            "Personal portfolio website",
            "Responsive landing page for a startup",
            "Interactive to-do app with local storage",
        ],
    },
    "Backend Developer": {
        "description": (
            "A Backend Developer handles server-side logic, databases, APIs, "
            "and application architecture. They ensure data flows correctly "
            "between the frontend and underlying systems."
        ),
        "skills": [
            "Python / Java / Node.js",
            "Flask or Django (Python)",
            "RESTful API design",
            "SQL (MySQL / PostgreSQL)",
            "Authentication & authorization basics",
            "Testing and debugging",
        ],
        "roadmap": [
            "Learn a backend language (Python recommended)",
            "Study database design and SQL",
            "Build REST APIs with Flask",
            "Learn about authentication and security",
            "Practice with database ORMs",
            "Deploy a backend service to a cloud platform",
        ],
        "projects": [
            "Student Management System API",
            "Blog platform with user authentication",
            "REST API for a library management system",
        ],
    },
    "Full Stack Developer": {
        "description": (
            "A Full Stack Developer works on both the frontend and backend of "
            "web applications. They can build complete, end-to-end solutions "
            "from database to user interface."
        ),
        "skills": [
            "HTML, CSS, JavaScript",
            "React or Angular",
            "Python Flask or Node.js",
            "REST API design",
            "MySQL / PostgreSQL",
            "Git and deployment (Heroku, Vercel)",
        ],
        "roadmap": [
            "Learn HTML, CSS, and JavaScript",
            "Master responsive design with Bootstrap",
            "Learn backend development with Flask",
            "Study database basics and SQL",
            "Build and consume REST APIs",
            "Deploy a full-stack project end to end",
        ],
        "projects": [
            "Student Management System",
            "Product Inventory System",
            "Online Course Portal",
        ],
    },
    "Mobile App Developer": {
        "description": (
            "A Mobile App Developer designs and builds applications for "
            "smartphones and tablets. They work with platforms like Android, "
            "iOS, or cross-platform frameworks."
        ),
        "skills": [
            "Kotlin / Swift / Dart",
            "Flutter or React Native",
            "Mobile UI/UX principles",
            "REST API integration",
            "Local data storage (SQLite, SharedPreferences)",
            "App publishing on Play Store / App Store",
        ],
        "roadmap": [
            "Learn Dart and Flutter (or Kotlin for Android)",
            "Understand mobile UI/UX design patterns",
            "Build simple apps (calculator, notes)",
            "Integrate REST APIs into your apps",
            "Learn state management",
            "Publish a complete app to the store",
        ],
        "projects": [
            "Notes app with local storage",
            "Weather app using a public API",
            "Budget tracker with charts",
        ],
    },
    "Data Analyst": {
        "description": (
            "A Data Analyst collects, processes, and interprets data to help "
            "organizations make informed decisions. They use statistics, "
            "visualization, and reporting tools."
        ),
        "skills": [
            "Python / R for data analysis",
            "Pandas and NumPy",
            "Data visualization (Matplotlib, Seaborn, Power BI)",
            "SQL for data querying",
            "Statistics and probability",
            "Excel and Google Sheets",
        ],
        "roadmap": [
            "Learn Python basics and Pandas",
            "Study statistics and probability",
            "Master data visualization with Matplotlib/Seaborn",
            "Learn SQL for data querying",
            "Practice with real-world datasets (Kaggle)",
            "Build a portfolio of analysis projects",
        ],
        "projects": [
            "Exploratory data analysis on a public dataset",
            "Sales dashboard with interactive charts",
            "Customer segmentation analysis",
        ],
    },
    "Machine Learning Engineer": {
        "description": (
            "A Machine Learning Engineer designs, builds, and deploys "
            "machine learning models. They bridge data science and software "
            "engineering to create intelligent systems."
        ),
        "skills": [
            "Python (NumPy, Pandas, Scikit-learn)",
            "Machine Learning algorithms",
            "Deep Learning (TensorFlow / PyTorch)",
            "Data preprocessing and feature engineering",
            "Model evaluation and optimization",
            "Git and MLOps basics",
        ],
        "roadmap": [
            "Master Python and numerical libraries",
            "Study core ML algorithms (regression, classification, clustering)",
            "Learn Scikit-learn and model evaluation",
            "Explore deep learning with TensorFlow or PyTorch",
            "Practice on Kaggle competitions",
            "Deploy a model as a web service",
        ],
        "projects": [
            "Spam email classifier",
            "House price prediction model",
            "Image classification with a neural network",
        ],
    },
    "Cybersecurity Analyst": {
        "description": (
            "A Cybersecurity Analyst protects computer systems and networks "
            "from threats. They monitor for vulnerabilities, investigate "
            "incidents, and implement security measures."
        ),
        "skills": [
            "Networking fundamentals (TCP/IP, DNS, HTTP)",
            "Operating systems security (Linux, Windows)",
            "Ethical hacking and penetration testing",
            "Cryptography basics",
            "Security tools (Wireshark, Nmap, Metasploit)",
            "Incident response and forensics",
        ],
        "roadmap": [
            "Learn networking fundamentals",
            "Study Linux command line and administration",
            "Understand common attack vectors",
            "Practice ethical hacking on platforms (TryHackMe)",
            "Learn cryptography and encryption basics",
            "Earn a security certification (CompTIA Security+)",
        ],
        "projects": [
            "Network vulnerability scanner script",
            "Password strength checker tool",
            "Log file analyzer for suspicious activity",
        ],
    },
    "Cloud/DevOps Engineer": {
        "description": (
            "A Cloud/DevOps Engineer manages cloud infrastructure, "
            "automates deployment pipelines, and ensures system reliability "
            "and scalability."
        ),
        "skills": [
            "Linux administration",
            "Cloud platforms (AWS / Azure / GCP)",
            "Docker and containerization",
            "CI/CD pipelines (GitHub Actions, Jenkins)",
            "Infrastructure as Code (Terraform)",
            "Monitoring and logging (Prometheus, Grafana)",
        ],
        "roadmap": [
            "Learn Linux and command-line basics",
            "Get familiar with a cloud platform (AWS free tier)",
            "Learn Docker for containerization",
            "Set up CI/CD pipelines with GitHub Actions",
            "Study Infrastructure as Code with Terraform",
            "Practice monitoring and incident response",
        ],
        "projects": [
            "Deploy a Flask app on AWS EC2 with Docker",
            "Automate deployments with a GitHub Actions pipeline",
            "Set up a monitoring dashboard with Grafana",
        ],
    },
    "UI/UX Designer": {
        "description": (
            "A UI/UX Designer focuses on how users interact with products. "
            "They research user needs, design interfaces, and create "
            "wireframes and prototypes to deliver intuitive experiences."
        ),
        "skills": [
            "Design thinking and user research",
            "Wireframing and prototyping (Figma, Adobe XD)",
            "Visual design and typography",
            "HTML/CSS basics for implementation",
            "Usability testing",
            "Interaction design principles",
        ],
        "roadmap": [
            "Learn design thinking principles",
            "Master a design tool like Figma",
            "Study color theory, typography, and layout",
            "Create wireframes and interactive prototypes",
            "Conduct usability testing with real users",
            "Build a professional design portfolio",
        ],
        "projects": [
            "Redesign a popular website (case study)",
            "Design a mobile app from concept to prototype",
            "Create a design system for a small product",
        ],
    },
    "Database Administrator": {
        "description": (
            "A Database Administrator manages, organizes, and secures "
            "databases. They ensure data integrity, optimize performance, "
            "and handle backups and recovery."
        ),
        "skills": [
            "SQL (advanced queries, joins, indexing)",
            "Database design and normalization",
            "MySQL / PostgreSQL / SQL Server",
            "Database security and access control",
            "Backup and recovery procedures",
            "Performance tuning and optimization",
        ],
        "roadmap": [
            "Learn SQL fundamentals and advanced queries",
            "Study database design and normalization",
            "Gain hands-on experience with MySQL or PostgreSQL",
            "Learn about indexing and query optimization",
            "Study backup, recovery, and replication",
            "Practice database administration tasks",
        ],
        "projects": [
            "Design and normalize a university database",
            "Build a database backup automation script",
            "Optimize slow queries in a sample database",
        ],
    },
}

# Subject-to-career affinity mapping (used in feature explanation)
SUBJECT_AFFINITY = {
    "Web Development": ["Frontend Developer", "Full Stack Developer"],
    "Design": ["UI/UX Designer", "Frontend Developer"],
    "Human-Computer Interaction": ["UI/UX Designer"],
    "Data Structures": ["Backend Developer"],
    "Algorithms": ["Backend Developer", "Machine Learning Engineer"],
    "Database Systems": ["Backend Developer", "Full Stack Developer", "Database Administrator"],
    "Software Engineering": ["Full Stack Developer", "Mobile App Developer"],
    "Mobile Development": ["Mobile App Developer"],
    "UI Design": ["Mobile App Developer", "UI/UX Designer"],
    "Statistics": ["Data Analyst"],
    "Data Science": ["Data Analyst", "Machine Learning Engineer"],
    "Business Analytics": ["Data Analyst"],
    "Artificial Intelligence": ["Machine Learning Engineer"],
    "Machine Learning": ["Machine Learning Engineer"],
    "Deep Learning": ["Machine Learning Engineer"],
    "Network Security": ["Cybersecurity Analyst"],
    "Ethical Hacking": ["Cybersecurity Analyst"],
    "Cryptography": ["Cybersecurity Analyst"],
    "Cloud Computing": ["Cloud/DevOps Engineer"],
    "DevOps": ["Cloud/DevOps Engineer"],
    "System Administration": ["Cloud/DevOps Engineer"],
    "Psychology": ["UI/UX Designer"],
    "SQL": ["Database Administrator"],
    "Data Management": ["Database Administrator"],
}


# ---------------------------------------------------------------------------
# Helper: build explanation from inputs and prediction
# ---------------------------------------------------------------------------
def build_explanation(form_data, predicted_path):
    """Build a human-readable explanation for the prediction."""
    reasons = []

    programming = int(form_data.get("programming_score", 50))
    math = int(form_data.get("math_score", 50))
    web = int(form_data.get("web_interest", 5))
    mobile = int(form_data.get("mobile_interest", 5))
    ai = int(form_data.get("ai_interest", 5))
    db = int(form_data.get("database_interest", 5))
    network = int(form_data.get("networking_interest", 5))
    cloud = int(form_data.get("cloud_interest", 5))
    design = int(form_data.get("design_interest", 5))
    subject = form_data.get("preferred_subject", "")

    if predicted_path in ("Frontend Developer", "Full Stack Developer"):
        if web >= 7:
            reasons.append("Your high web development interest aligns well with this path.")
        if programming >= 65:
            reasons.append("Your strong programming skills provide a solid foundation.")
    elif predicted_path == "Backend Developer":
        if programming >= 65:
            reasons.append("Your strong programming skills are ideal for backend work.")
        if db >= 5:
            reasons.append("Your database interest supports server-side development.")
    elif predicted_path == "Mobile App Developer":
        if mobile >= 7:
            reasons.append("Your strong mobile app interest is a great indicator.")
    elif predicted_path == "Data Analyst":
        if math >= 60:
            reasons.append("Your strong math skills support data analysis work.")
        if db >= 6:
            reasons.append("Your database interest helps with querying and managing data.")
    elif predicted_path == "Machine Learning Engineer":
        if math >= 70:
            reasons.append("Your excellent math skills are critical for ML work.")
        if ai >= 8:
            reasons.append("Your high AI/ML interest strongly matches this career.")
    elif predicted_path == "Cybersecurity Analyst":
        if network >= 8:
            reasons.append("Your networking interest is a key trait for cybersecurity.")
    elif predicted_path == "Cloud/DevOps Engineer":
        if cloud >= 8:
            reasons.append("Your strong cloud interest is a perfect match.")
    elif predicted_path == "UI/UX Designer":
        if design >= 8:
            reasons.append("Your high design interest aligns with UI/UX work.")
        if communication >= 60:
            reasons.append("Your communication skills support user research.")
    elif predicted_path == "Database Administrator":
        if db >= 8:
            reasons.append("Your strong database interest is ideal for this path.")

    # Subject-based reason
    if subject in SUBJECT_AFFINITY:
        if predicted_path in SUBJECT_AFFINITY[subject]:
            reasons.append(
                f'Your preferred subject "{subject}" directly relates to this career.'
            )

    if not reasons:
        reasons.append(
            "Based on the overall pattern of your scores and interests, "
            f"{predicted_path} was identified as the best fit."
        )

    return reasons


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Render the home page with the student input form."""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """Process the submitted form and return the ML prediction."""
    # Collect form data
    form_data = {
        "name": request.form.get("name", "Student"),
        "age": request.form.get("age", "20"),
        "department": request.form.get("department", "Computer Science"),
        "math_score": request.form.get("math_score", 50),
        "programming_score": request.form.get("programming_score", 50),
        "communication_score": request.form.get("communication_score", 50),
        "problem_solving_score": request.form.get("problem_solving_score", 50),
        "web_interest": request.form.get("web_interest", 5),
        "mobile_interest": request.form.get("mobile_interest", 5),
        "ai_interest": request.form.get("ai_interest", 5),
        "database_interest": request.form.get("database_interest", 5),
        "networking_interest": request.form.get("networking_interest", 5),
        "cloud_interest": request.form.get("cloud_interest", 5),
        "design_interest": request.form.get("design_interest", 5),
        "preferred_subject": request.form.get("preferred_subject", "Web Development"),
        "career_goal": request.form.get("career_goal", ""),
    }

    # Check model availability
    if model is None or label_encoder is None:
        return render_template(
            "result.html",
            error="Model not trained yet. Please run train_model.py first.",
            form_data=form_data,
        )

    try:
        # Encode categorical features
        preferred_subject = form_data["preferred_subject"]
        career_goal = form_data["career_goal"]

        # Encode preferred_subject
        if preferred_subject in label_encoder.classes_:
            subject_encoded = 0  # fallback
        else:
            # We need a separate encoder for subject; reuse the target encoder
            # as a simple approach since categories overlap in our dataset.
            # In production, you would save dedicated encoders.
            from sklearn.preprocessing import LabelEncoder
            temp_le = LabelEncoder()
            temp_le.fit(
                [
                    "Web Development", "Design", "Human-Computer Interaction",
                    "Data Structures", "Algorithms", "Database Systems",
                    "Software Engineering", "Mobile Development", "UI Design",
                    "Statistics", "Data Science", "Business Analytics",
                    "Artificial Intelligence", "Machine Learning", "Deep Learning",
                    "Network Security", "Ethical Hacking", "Cryptography",
                    "Cloud Computing", "DevOps", "System Administration",
                    "Psychology", "SQL", "Data Management",
                ]
            )
            if preferred_subject in temp_le.classes_:
                subject_encoded = int(temp_le.transform([preferred_subject])[0])
            else:
                subject_encoded = 0

        # Encode career_goal
        temp_le2 = LabelEncoder()
        all_goals = [
            "Build beautiful websites", "Build scalable systems",
            "Build complete applications", "Build mobile apps",
            "Analyze data for insights", "Build AI systems",
            "Protect systems from attacks", "Manage cloud infrastructure",
            "Design user experiences", "Manage large databases",
            "Create interactive UIs", "Work at a tech startup",
            "Work on server-side logic", "Become a software architect",
            "Work independently", "Lead development teams",
            "Work at a tech company", "Launch own app",
            "Work in business intelligence", "Become a data scientist",
            "Research new algorithms", "Work at a research lab",
            "Work in security operations", "Become a security consultant",
            "Automate deployments", "Work at a cloud provider",
            "Work at a design agency", "Become a product designer",
            "Optimize database performance", "Work as a DBA",
        ]
        if career_goal in all_goals:
            temp_le2.fit(all_goals)
            goal_encoded = int(temp_le2.transform([career_goal])[0])
        else:
            goal_encoded = 0

        # Build feature vector
        features = np.array(
            [
                [
                    int(form_data["math_score"]),
                    int(form_data["programming_score"]),
                    int(form_data["communication_score"]),
                    int(form_data["problem_solving_score"]),
                    int(form_data["web_interest"]),
                    int(form_data["mobile_interest"]),
                    int(form_data["ai_interest"]),
                    int(form_data["database_interest"]),
                    int(form_data["networking_interest"]),
                    int(form_data["cloud_interest"]),
                    int(form_data["design_interest"]),
                    subject_encoded,
                    goal_encoded,
                ]
            ]
        )

        # Predict
        prediction_encoded = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]

        predicted_path = label_encoder.inverse_transform([prediction_encoded])[0]
        confidence = float(np.max(probabilities)) * 100

        # Get career details
        details = CAREER_DETAILS.get(predicted_path, {})

        # Build explanation
        explanations = build_explanation(form_data, predicted_path)

        return render_template(
            "result.html",
            form_data=form_data,
            predicted_path=predicted_path,
            confidence=round(confidence, 2),
            description=details.get("description", ""),
            skills=details.get("skills", []),
            roadmap=details.get("roadmap", []),
            projects=details.get("projects", []),
            explanations=explanations,
            error=None,
        )

    except Exception as e:
        return render_template(
            "result.html",
            error=f"An error occurred during prediction: {str(e)}",
            form_data=form_data,
        )


@app.route("/about")
def about():
    """Render the about page."""
    return render_template("about.html")


@app.route("/health")
def health():
    """Return JSON health status for testing."""
    return jsonify(
        {
            "status": "running",
            "model_loaded": model is not None,
            "encoder_loaded": label_encoder is not None,
            "career_paths": list(CAREER_DETAILS.keys()),
        }
    )


# ---------------------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
