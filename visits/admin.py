from django.contrib import admin
from .models import ( visitModel, paymentModel, vitalsModel, complaintsModel, physicalExamsModel, comorbiditiesModel, investigationsModel, diagnosisModel,
    treatmentModel, remarksModel, merged )

admin.site.register(visitModel)
admin.site.register(paymentModel)
admin.site.register(vitalsModel)
admin.site.register(complaintsModel)
admin.site.register(physicalExamsModel)
admin.site.register(comorbiditiesModel)
admin.site.register(investigationsModel)
admin.site.register(diagnosisModel)
admin.site.register(treatmentModel)
admin.site.register(remarksModel)
admin.site.register(merged)
