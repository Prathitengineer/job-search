# Sample job data - in a real app, this would come from a database
sample_jobs = [
    {
        "id": 1,
        "title": "Senior Software Engineer",
        "company": "TechCorp",
        "location": "San Francisco",
        "remote": False,
        "experience": "5+",
        "description": "We're looking for an experienced software engineer..."
    },
    {
        "id": 2,
        "title": "Product Manager",
        "company": "InnovateCo",
        "location": "New York",
        "remote": False,
        "experience": "3-5",
        "description": "Lead our product development team..."
    },
    {
        "id": 3,
        "title": "UX Designer",
        "company": "DesignHub",
        "location": "Remote",
        "remote": True,
        "experience": "1-3",
        "description": "Create beautiful user experiences..."
    },
    {
        "id": 4,
        "title": "Senior Software Engineer",
        "company": "TechCorp",
        "location": "San Francisco",
        "remote": False,
        "experience": "5+",
        "description": "We're looking for an experienced software engineer..."
    },
    {
        "id": 5,
        "title": "Product Manager",
        "company": "InnovateCo",
        "location": "New York",
        "remote": False,
        "experience": "3-5",
        "description": "Lead our product development team..."
    },
    {
        "id": 6,
        "title": "UX Designer",
        "company": "DesignHub",
        "location": "Remote",
        "remote": True,
        "experience": "1-3",
        "description": "Create beautiful user experiences..."
    }
]

current_user = {
    'id': '',
    'name': '',
    'email': '',
    'phone': '',
    'location': '',
    'role': 'job_seeker'  # or 'recruiter'
}

posted_jobs = []