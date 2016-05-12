from rest_framework import serializers
from telco_service.models import *

class GenderStatsSerializer( serializers.Serializer ):
    # date_ts = serializers.DateField()
    # gender = serializers.CharField()
    # impr_count = serializers.IntegerField()
    # clicks_count = serializers.IntegerField()
    # media_cost = serializers.IntegerField()
    # data_fees = serializers.IntegerField()
    # telco_share = serializers.IntegerField()
    # telco_id = serializers.IntegerField()
    impr_data = serializers.ListField()
    clicks_data = serializers.ListField()
    media_cost_data = serializers.ListField()
    data_fees_data = serializers.ListField()
    telco_share_data = serializers.ListField()

    # class Meta:
    #     model = GenderStats
    #     fields = ( 'date_ts', 'gender', 'impr_count', 'clicks_count', 'media_cost', 'data_fees', 'telco_share', 'telco_id' )