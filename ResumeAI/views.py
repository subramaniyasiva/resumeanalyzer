from django.shortcuts import render
import PyPDF2
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import CVAppData

nltk.download('wordnet')
nltk.download('omw-1.4')  
r=""

def landing(request):
    return render(request,'landingpage.html')
# Create your views here.
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stopwords.words('english')]
    return " ".join(words)
def read_content(f):
    pdf_reader=PyPDF2.PdfReader(f)
    content=""
    for x in pdf_reader.pages:
        content+=x.extract_text() or ""
    return content
def home(request):
    results = []

    if request.method == 'POST':
        jd = request.POST.get('jd')
        jd = clean_text(jd)
        cvs = request.FILES.getlist('resume')

        for cv_file in cvs:
            file_data = read_content(cv_file)
            cv_text = clean_text(file_data)

            docs = [cv_text, jd]

            if all(docs):
                vectorizer = TfidfVectorizer()
                vectors = vectorizer.fit_transform(docs)

                sim_matrix = cosine_similarity(vectors[-1], vectors[:-1])
                r = "Ideal Candidate" if (sim_matrix*100).max() > 10 else "Not Recommended"

                obj = CVAppData(
                    job_desc=jd,
                    cv_file=cv_file.name,
                    result=str(sim_matrix),
                    output=r 
                )
                obj.save()

                # append structured data
                results.append({'filename': cv_file.name, 'result': r})
            else:
                results.append({'filename': cv_file.name, 'result': 'Error processing'})

    return render(request, 'home.html', {'results': results})

def experienced(request):
    return home(request)