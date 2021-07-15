# from django.http import HttpResponse
# from django.shortcuts import render
# from .models import FilesUpload
# import PyPDF2
#
# from django.core.files.storage import FileSystemStorage
# Create your views here
# def uploadfile_view(request):
#     if request.method == "POST":
#         f=request.FILES['file']
#         fs = FileSystemStorage()
#         filename,ext=str(f).split('.')
#         file = fs.save(str(f),f)
#         fileurl = fs.url(file)
#         size=fs.size(file)
#         return render(request,'index.html',{'fileUrl':fileurl,fileName:filename,
#                                             "ext":ext,"size":size})
#     else:
#         return render(request,'index.html',{})
# def home(request):
#     if request.method == "POST":
#         file2 = request.FILES["file"]
#         # document = FilesUpload.objects.create(file=file2)
#         pdfReader = PyPDF2.PdfFileReader(file2)
#         # print(" No. Of Pages :", pdfReader.numPages)
#         pageObject = pdfReader.getPage(0)
#         # print(pageObject.extractText())
#         return HttpResponse(pageObject.extractText())
#     return render(request, "index.html")

# import PyPDF2
import re
import pdfplumber
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer
import nltk

class uploadpdf(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        # content_type = file_uploaded.content_type
        # response = "POST API and you have uploaded a {} file".format(content_type)

        # pdfReader = PyPDF2.PdfFileReader(file_uploaded)
        # pageObj = pdfReader.getPage(0)
        # # print(pageObj.extractText())



        pdf = pdfplumber.open(file_uploaded)
        page = pdf.pages[0]
        text = page.extract_text()

        # def extract_mobile_number(text):
        #     phone = re.findall(re.compile(
        #         r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'),
        #                        text)
        #
        #     if phone:
        #         number = ''.join(phone[0])
        #         if len(number) > 10:
        #             return '+' + number
        #         else:
        #             return number
        PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')

        def extract_phone_number(resume_text):
            phone = re.findall(PHONE_REG, resume_text)

            if phone:
                number = ''.join(phone[0])

                if resume_text.find(number) >= 0 and len(number) < 16:
                    return number
            return None

        print(extract_phone_number(text))

        # def extract_email(text):
        #     email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", text)
        #     if email:
        #         try:
        #             return email[0].split()[0].strip(';')
        #         except IndexError:
        #             return None
        EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')

        def extract_emails(resume_text):
            return re.findall(EMAIL_REG, resume_text)



        def extract_names(text):
            person_names = []
            for sent in nltk.sent_tokenize(text):
                for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                    if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                        person_names.append(' '.join(chunk_leave[0] for chunk_leave in chunk.leaves()))
            return person_names

        #print("email id:-", extract_email(text))
        SKILLS = [
            'Auto card',
            'auto card',
            'SolidWorks',
            'Ansys',
            'Automation Studio',

        ]

        def extract_skills(text):
            stop_words = set(nltk.corpus.stopwords.words('english'))
            word_tokens = nltk.tokenize.word_tokenize(text)

            filtered_tokens = [w for w in word_tokens if w not in stop_words]

            filtered_tokens = [w for w in word_tokens if w.isalpha()]

            bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

            found_skills = set()

            for token in filtered_tokens:
                if token in SKILLS:
                    found_skills.add(token)

            for ngram in bigrams_trigrams:
                if ngram in SKILLS:
                    found_skills.add(ngram)

            return found_skills

        m=(extract_names(text)[1],extract_emails(text),extract_phone_number(text),extract_skills(text))
        return Response(m)