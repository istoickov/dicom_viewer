import random
import imageio

import matplotlib.pyplot as plt

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from .forms import FileForm
from .models import DicomImages


RESPONSES = [
    {
        "status_code": 200,
        "message": "OK",
        "perspective": {
            "id": 1,
            "value": "Short Axis PSAXA Zoomed Aorta 1"
        }
    },
    {
        "status_code": 200,
        "message": "OK",
        "perspective": {
            "id": 2,
            "value": "Short Axis PSAXA Zoomed Aorta 2"
        }
    },
    {
        "status_code": 200,
        "message": "OK",
        "perspective": {
            "id": 3,
            "value": "Short Axis PSAXA Zoomed Aorta 3"
        }
    },
    {
        "status_code": 200,
        "message": "OK",
        "perspective": {
            "id": 4,
            "value": "Short Axis PSAXA Zoomed Aorta 4"
        }
    },
    {
        "status_code": 500,
        "message": "ERROR",
    },
]


def upload(request):
    context = {'form': None, 'last': None}

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            context['last'] = '\n'.join([f.name for f in request.FILES.getlist('file')])

            files = request.FILES.getlist('file')
            processed_files = []

            for file in files:
                with open("uploads/{}".format(file.name), 'wb+') as f:
                    for chunk in file.chunks():  # Write in chunks; large files won't use a lot of RAM
                        f.write(chunk)

                info = {}

                if file.name[-3:] == 'dcm':
                    fs = FileSystemStorage()
                    filename = fs.save(file.name, file)
                    info['name'] = filename

                    if filename[-3:].upper() == 'DCM':
                        dcpimg = imageio.imread(f"uploads/{filename}")

                        if len(dcpimg.shape) == 4:
                            dcpimg = dcpimg[0, 0]
                        elif len(dcpimg.shape) == 3:
                            dcpimg = dcpimg[0]

                        for keys in dcpimg.meta:
                            info[keys] = str(dcpimg.meta[keys])

                    fs.delete(filename)

                    fig = plt.gcf()
                    fig.set_size_inches(18.5, 10.5)
                    plt.imshow(dcpimg, cmap='gray')
                    plt.colorbar()
                    plt.savefig(f"media/{filename[:-3]}jpg", format="jpg", dpi=300)
                    plt.close()

                uid = info["SOPInstanceUID"]
                dicom_images = DicomImages.objects.all()
                if uid not in [item.uid for item in dicom_images]:
                    response = random.choice(RESPONSES)
                    if response["status_code"] == 200:
                        response_val = response["perspective"]["value"]

                        DicomImages(
                            uid=info["SOPInstanceUID"],
                            response=response_val
                        ).save()
                else:
                    response_val = DicomImages.objects.filter(uid__exact=uid).first().response

                info["Response value"] = response_val
                processed_files.append({
                    'info': info,
                    'url': f"media/{filename[:-3]}jpg"
                })

            context['imgs'] = processed_files
    else:
        form = FileForm()

    context['form'] = form
    return render(request, 'upload/index.html', context)
