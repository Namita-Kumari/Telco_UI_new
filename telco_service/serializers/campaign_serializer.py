from rest_framework import serializers
from telco_service.models import *

class CampaignStatsSerializer( serializers.ModelSerializer ):
    class Meta:
        model = CampaignStats
        fields = ( 'date_ts', 'name', 'status', 'impr_count', 'clicks_count', 'media_cost', 'revenue_model', 'payout', 'revenue', 'data_fees', 'telco_share', 'telco_id', 'ecpc', 'ecpm', 'tot_bids', 'ctr' )



class CampaginEntitySerializer( serializers.Serializer ):
    data = serializers.ListField()



class OverllStatsSerializer( serializers.Serializer ):
    total_impr = serializers.IntegerField()
    total_clicks = serializers.IntegerField()
    total_media_cost = serializers.IntegerField()
    total_revenue = serializers.IntegerField()
    total_data_fees = serializers.IntegerField()
    total_telco_share = serializers.IntegerField()
    total_ecpc = serializers.FloatField()
    total_ecpm = serializers.FloatField()
    total_ctr = serializers.FloatField()
    cumulative_bids = serializers.IntegerField()
    total_win_rate = serializers.FloatField()
    # daily_stats = serializers.JSONField()
    dates_list = serializers.ListField()
    impr_data = serializers.ListField()
    clicks_data = serializers.ListField()
    media_cost_data = serializers.ListField()
    data_fees_data = serializers.ListField()
    telco_share_data = serializers.ListField()


class CampaignReportSerializer( serializers.Serializer ):
    name = serializers.CharField( required= False )
    date_ts = serializers.CharField(required=False)
    entity_level_report = serializers.ListField()
    impr_count = serializers.IntegerField()
    clicks_count = serializers.IntegerField()
    ctr = serializers.FloatField()
    media_cost = serializers.IntegerField()
    telco_share = serializers.IntegerField()
    payout = serializers.IntegerField( required = False )
    revenue_model = serializers.CharField( required = False )
    column_list = serializers.ListField()







