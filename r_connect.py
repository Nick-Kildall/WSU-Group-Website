from app import create_app, db
from app.Model.models import Interest

app = create_app()

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if Interest.query.count() == 0:
        interests = ['Artificial Intelligence/Machine Learning','Front End Developement', 'Back End Developement', 'Data Science', 'Software Engineering',
            'Web Development', 'Full Stack', 'Mobile Application', 'Game Development', 'Cybersecurity', 'Financial Analysis', 'Blockchain']
        for i in interests:
            db.session.add(Interest(name=i))
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)