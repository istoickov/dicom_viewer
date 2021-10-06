# Dicom Images Uploader

# Setup
* Install Python and run the project

## Create virtualenv
    virtualenv -p python3 .venv

## Activate the .venv
    source .venv/bin/activate

## Instal requirements
    pip install -r requirements.txt

## Make migrations and migrate
    python manage.py makemigrations
    python manage.py migrate

## Create superuser
    python manage.py createsuperuser

## Run dev server
    python manage.py runserver

## Model/s
    class DicomImages(models.Model):
        file = models.FileField()
        uid = models.TextField()
        response = models.TextField()
        upload_date = models.DateTimeField(auto_now_add=True)

## View/s
    def upload(request):
        ...
        
        processed_files.append({
            'info': info,
            'url': f"media/{filename[:-3]}jpg"
        })
        context['imgs'] = processed_files
        
        ...
        
        context['form'] = form
        
        return render(request, 'upload/index.html', context)

## Url/s
    http://127.0.0.1:8000/

## Form
    class FileForm(forms.ModelForm):
        label = ''
    
        class Meta:
            model = DicomImages
            fields = ('file',)
            widgets = {
                'file': forms.ClearableFileInput(attrs={'multiple': True})
            }

Gives you the index template, which has **browse** and **upload** button. After choosing needed files, click on upload and tables and rendered `.jpg` will be shown from the uploaded _**dicom**_ file/s.