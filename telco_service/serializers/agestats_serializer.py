from rest_framework import serializers
from telco_service.models import *

class AgeStatsSerializer( serializers.Serializer ):
    impr_count = serializers.ListField()
    clicks_count = serializers.ListField()
    media_cost = serializers.ListField()
    data_fees = serializers.ListField()
    telco_share = serializers.ListField()



    # class Meta:
    #     model = AgeStats
    #     fields = ( 'date_ts', 'age_group', 'impr_count', 'clicks_count', 'media_cost', 'data_fees', 'telco_share', 'telco_id' )