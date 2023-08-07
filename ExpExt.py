import spacy
import streamlit as st
from spacy.matcher import Matcher

# Load the 'en_core_web_sm' model
nlp = spacy.load('en_core_web_sm')

# Scoring dictionary
entity_scores = {
    "Internship": 5,
    "ORG": 3,
    "TITLE": 2,
    "TECHNOLOGY": 1,
    "SKILL": 1,
    "EXPERIENCE": 2,
}

internship_titles = [
    "Software Development Intern",
    "Data Science Intern",
    "Web Development Intern",
    "Machine Learning Intern",
    "Artificial Intelligence (AI) Intern",
    "Cybersecurity Intern",
    "IT Support Intern",
    "Network Engineering Intern",
    "UX/UI Design Intern",
    "Mobile App Development Intern",
    "Cloud Computing Intern",
    "Database Management Intern",
    "DevOps Intern",
    "Quality Assurance (QA) Intern",
    "Game Development Intern",
    "Marketing Intern",
    "Sales Intern",
    "Business Development Intern",
    "Finance Intern",
    "Human Resources (HR) Intern",
    "Supply Chain Intern",
    "Operations Intern",
    "Project Management Intern",
    "Market Research Intern",
    "Data Analysis Intern",
    "Product Management Intern",
    "Digital Marketing Intern",
    "Social Media Intern",
    "Customer Relations Intern",
    "E-commerce Intern",
]


skills_titles = [
    # Programming Languages
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "SQL",
    "HTML",
    "CSS",
    "Ruby",
    "Swift",
    "C#",
    "PHP",
    "Go",
    "Kotlin",

    # Data Analysis and Machine Learning
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "Scikit-learn",
    "TensorFlow",
    "Keras",
    "PyTorch",

    # Web Development
    "React",
    "Angular",
    "Vue.js",
    "Node.js",
    "Express.js",
    "Django",
    "Flask",
    "RESTful API Design",
    "GraphQL",

    # Database Management
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "SQLite",
    "Oracle",

    # Cloud Computing
    "Amazon Web Services (AWS)",
    "Microsoft Azure",
    "Google Cloud Platform (GCP)",

    # DevOps and CI/CD
    "Docker",
    "Kubernetes",
    "Jenkins",
    "Git",
    "Travis CI",

    # Cybersecurity
    "Network Security",
    "Ethical Hacking",
    "Vulnerability Assessment",
    "Penetration Testing",

    # Project Management
    "Agile Methodology",
    "Scrum",
    "Kanban",
    "Jira",

    # Marketing and Digital Marketing
    "Social Media Marketing",
    "Search Engine Optimization (SEO)",
    "Content Marketing",
    "Email Marketing",
    "Google Analytics",

    # Business Analysis
    "Market Research",
    "Business Intelligence (BI)",
    "Data Visualization",

    # Financial Analysis
    "Financial Modeling",
    "Budgeting",
    "Forecasting",
    "Financial Reporting",

    # Communication and Presentation
    "Public Speaking",
    "Written Communication",
    "Visual Communication",
    "Microsoft PowerPoint",

    # Time Management and Organization
    "Project Planning",
    "Task Prioritization",
    "Time Tracking",

    # Problem-Solving and Critical Thinking
    "Analytical Thinking",
    "Decision Making",
    "Troubleshooting",

    # Leadership and Team Management
    "Leadership Skills",
    "Teamwork",
    "Conflict Resolution",

    # Language Skills
    "Fluency in multiple languages (e.g., English, Spanish, Mandarin, etc.)",

    # Soft Skills
    "Communication",
    "Time Management",
    "Adaptability",
    "Creativity",
    "Problem Solving",
    "Critical Thinking",
    "Leadership",
    "Teamwork",
    "Conflict Resolution",
    "Negotiation",
    "Empathy",
    "Work Ethic",
    "Attention to Detail",
    "Organization",
    "Dependability",
    "Flexibility",
    "Interpersonal Skills",
    "Presentation Skills",
    "Networking",
    "Customer Service",
    "Emotional Intelligence",
    "Confidence",
]

leadership_patterns = [
    [{"LOWER": "president"}],
    [{"LOWER": "vice"}, {"LOWER": "president"}],
    [{"LOWER": "vice"}, {"LOWER": {"IN": ["president", "president,"]}}, {"POS": "PROPN", "OP": "?"}],  # Handles variations like "Vice President John"
    [{"LOWER": {"IN": ["vice-president", "vp"]}}],
    [{"LOWER": "financial"}, {"LOWER": "controller"}],
    [{"LOWER": {"IN": ["honorary", "honorary,"]}}, {"LOWER": "general"}, {"LOWER": "secretary"}],
    [{"LOWER": {"IN": ["chairperson", "chairman", "chairwoman", "chair", "chair,"]}}],
    [{"LOWER": {"IN": ["headmaster", "headmistress", "principal", "principal,"]}}],
]


# Create the Matcher and add all patterns
matcher = Matcher(nlp.vocab)
# Add patterns for internships
for title in internship_titles:
    matcher.add("InternshipPattern", [[{"LOWER": {"IN": [title.lower(), "intern"]}}]])


# Add pattern for sentences like "I was a (internship title) intern at XYZ"
matcher.add("InternshipPattern", [[{"LOWER": "i"}, {"LOWER": "was"}, {"LOWER": "a"}, {"LOWER": {"IN": internship_titles}}, {"LOWER": "intern"}, {"LOWER": "at"}, {"ENT_TYPE": "ORG"}]])

for title in internship_titles:
    matcher.add("InternshipPattern", [[{"LOWER": {"IN": [title.lower(), "intern"]}}]])

for title in skills_titles:
    matcher.add("SkillPattern", [[{"LOWER": title.lower()}]])

for pattern in leadership_patterns:
    matcher.add("LeadershipPattern", [pattern])

# Streamlit app
st.title("Experience and Skills Extractor")

response = st.text_area("Enter your response:")
if st.button("Extract"):
    # Preprocessing
    response = response.lower()  # Convert to lowercase
    doc = nlp(response)

    # Custom entity matching for internships, skills, and leadership roles
    matches = matcher(doc)
    internships = []
    organizations = []
    skills = []
    leadership_roles = []
    internship_sentences = []  # To store sentences containing the word "intern"
    for sent in doc.sents:
        if "intern" in sent.text.lower():  # Check if the word "intern" is present in the sentence
            internship_sentences.append(sent.text)

    for match_id, start, end in matches:
        span = doc[start:end]
        if doc.vocab.strings[match_id] == "InternshipPattern":
            internships.append(span.text)
            # Get the word before "INTERN" and display it in Streamlit
            word_before_intern = doc[start - 1].text if start > 0 else None
            if word_before_intern:
                st.info(f"Word before 'INTERN': {word_before_intern}")
        elif doc.vocab.strings[match_id] == "ORG":
            organizations.append(span.text)
        elif doc.vocab.strings[match_id] == "SkillPattern":
            skills.append(span.text)
        elif doc.vocab.strings[match_id] == "LeadershipPattern":
            leadership_roles.append(span.text)

    # Print the extracted internship information (if found)
    if internships:
        st.success("Extracted Internship: " + internships[0])  # Assuming we are interested in the first internship found
    else:
        st.warning("No internships found in the response.")

    # Print the extracted organization names (if found)
    if organizations:
        st.success("Organizations: " + ", ".join(organizations))

    # Print the extracted skills (if found)
    if skills:
        st.success("Skills: " + ", ".join(skills))

    # Print the extracted leadership roles (if found)
    if leadership_roles:
        st.success("Leadership Roles: " + ", ".join(leadership_roles))

    # Print sentences containing the word "intern"
    if internship_sentences:
        st.subheader("Sentences with the word 'intern':")
        for sentence in internship_sentences:
            st.write(sentence)

    # Named Entity Recognition (NER) for other entities and scoring
    for ent in doc.ents:
        entity_label = ent.label_
        score = entity_scores.get(entity_label, 0)
        if entity_label not in ["Internship", "ORG", "SKILL", "LeadershipPattern"]:
            st.info(f"{entity_label}: {ent.text} - Score: {score}")
