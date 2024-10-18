from django.shortcuts import render, redirect,HttpResponse
from django.conf import settings

#from csv_project import csv_project
from .forms import CSVUploadForm
from .models import Company
import pandas as pd
import os
from sqlalchemy import create_engine

# Create your views here.
def upload_csv(request):
    try:
        print("request is",request)
        print("request.POST is",request.POST)
        print("request.FILES is",request.FILES)
        if request.method == 'POST':
            form = CSVUploadForm(request.POST, request.FILES)
            print("form is",form)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                print("csv_file is",csv_file)
                # filepath = os.path.join(settings.MEDIA_ROOT, csv_file.name)
                # print("filepath is",filepath)
                # with open(filepath, 'wb+') as destination:
                #     for chunk in csv_file.chunks():
                #         destination.write(chunk)    
                df = pd.read_csv(csv_file)
                print("df is",df)
                print("type of df is",type(df))
                df["year founded"]= df['year founded'].fillna(0)
                df["current employee estimate"]= df['current employee estimate'].fillna(0)
                df["total employee estimate"]= df['total employee estimate'].fillna(0)
                # print("df is", df.heads())
                data=list(Company(name=i["name"],
    domain=i["domain"],
    year_founded=int(i["year founded"]),
    industry=i["industry"],
    size_range=i["size range"],
    locality=i["locality"],
    country=i["country"],
    linkedin_url=i["linkedin url"],
    current_employee_estimate=int(i["current employee estimate"]),
    total_employee_estimate=int(i["total employee estimate"])) for i in df.to_dict("records"))

                Company.objects.bulk_create(data)
                return HttpResponse("Csv Uploaded")

                # #df.to_sql('companies', con=create_engine('sqlite:///db.sqlite3'), if_exists='replace', index=False)

                # # db_engine = create_engine(str(settings.DATABASES['default']['ENGINE']) + '://' +
                # #                           #str(settings.DATABASES['default']['USER']) + ':' +
                # #                           #str(settings.DATABASES['default']['PASSWORD']) + '@' +
                # #                          # str(settings.DATABASES['default']['HOST']) + '/' +
                # #                           str(settings.DATABASES['default']['NAME']))

                # # Create SQLAlchemy engine for SQLite
                # db_path = settings.DATABASES['default']['NAME']  # Path to SQLite DB
                # db_engine = create_engine(f'sqlite:///{db_path}')  # Correct SQLite connection URL format
                # # (df.to_dict())
                # df.to_sql('csv_uploader_person', con=db_engine, if_exists='append', index=False)
                return redirect('upload_success')
        else:
            form = CSVUploadForm()
        return render(request, 'upload.html', {'form': form})
    except Exception as e :
        print(e)
        return HttpResponse({"message":str(e)})


def upload_success(request):
    return render(request, 'success.html')


# df = pd.read_csv(r"C:\Users\admin\Desktop\Siddharth\Django_Projects\CSV_Uploader\csv_project\media\companies_sorted.csv")
# # print("df is", df.heads())
# data=list()
# for i in df.to_dict("records"):
#     print(i["name"])



