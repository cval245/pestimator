from django.shortcuts import render
from rest_framework import generics
# Create your views here.

class BaseCountryForm(generics.GenericAPIView):
	pass

# need to include
# filing estimate template
# publication estimate template
# oaestimatetemplate
# allowancetemplate
# issuetemplate
# conditions for each
# law_firm_est_template for each

# filingTransform
# publtransform
# oatransform
# allowanceTransform
# issueTransform

# country
# countryOANum

# one form of doom???
# or partial forms that are aggregated?
