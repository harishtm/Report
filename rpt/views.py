from django.http import Http404,HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from rpt.forms import *
from django.views.generic import View
from reportlab.pdfgen import canvas
from django.contrib.auth.models import User
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch

from reportlab.lib.enums import TA_RIGHT,TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter, A4
from io import BytesIO
from Report.settings import *

# Register Fonts
pdfmetrics.registerFont(TTFont('Arial', STATICFILES_DIRS[0] + '/fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', STATICFILES_DIRS[0] + '/fonts/arialbd.ttf'))


# A large collection of style sheets pre-made for us
styles = getSampleStyleSheet()
# Our Custom Style
styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))


 
class MyPrint:
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize



def add_student(request):
    form = StudentForm()
    if request.method == "POST":
        form = StudentForm(request.POST,request.FILES)
        form.save()
    return render(request,'add_student.html',locals())


def student_list(request):
    student_list = Student.objects.all()
    return render(request,'student_list.html',locals())


class PrintView(View):

    template_name = "student_list.html"

    def get(self, request, *args, **kwargs):
    
        pdf = print_users(self)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="My Users.pdf"'
        response.write(pdf)
        return response
    
    #return response






def print_users(self):

    buffer = BytesIO()
    #buffer = self.buffer
    doc = SimpleDocTemplate(buffer,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=72,
                            pagesize=A4)

    student_obj = Student.objects.get(id=int(self.kwargs['stid']))

    elements = []

    #I = Image(STATICFILES_DIRS[0] +"/"+ student_obj.image.url_90x120)
    I = Image(student_obj.image)
    data= [
            ['Student Name', 'Student Age', 'Student Address','Image'],
            [student_obj.name, student_obj.age, student_obj.address, I]
           ]

    t=Table(data,4*[2*inch], 2*[1.3*inch])

    t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                           ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                           ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                           ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ]))
     
    elements.append(t)
    # write the document to disk
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


