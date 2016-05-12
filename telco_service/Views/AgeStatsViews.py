from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import viewsets, status
from telco_service.models import *
from django.db.models import Sum
from django.db.models.functions import Coalesce
from telco_service.serializers.agestats_serializer import AgeStatsSerializer
import sys, pdb

class AgeStatsViewSet( viewsets.ModelViewSet ):
    model = AgeStats
    serializer_class = AgeStatsSerializer
    queryset = AgeStats.objects.all()


    def list(self, request, *args, **kwargs):
        """
        Returns Age Stats
        """
        result = AgeStats.objects.all()
        if result:
            serializer = AgeStatsSerializer(result, many=True )
            return Response(serializer.data)
        else:
            return Response( "No Age Statistics found", status = status.HTTP_204_NO_CONTENT )


    def retrieve(self, request,pk=None, *args, **kwargs):
        """
        Returns Age Stats
        """
        age_group_list = [ "13-19", "20-30", "31-45", "46-55", "56-64", "65+" ]
        try:
            start_date = request.query_params[ 'start_date' ]
            end_date = request.query_params['end_date']
        except:
            err_msg = "Missing start date or end date both. Accepted date format : YYYY-MM-DD"
            return Response( err_msg, status =status.HTTP_500_INTERNAL_SERVER_ERROR )
        try:
            age_stats_info = AgeStats.objects.filter(date_ts__gte = start_date ).filter( date_ts__lte = end_date )
            if not age_stats_info:
                return Response( "Age stats not found in specified date range", status = status.HTTP_204_NO_CONTENT )
        except:
            err_msg = "Invalid date. Accepted date format : YYYY-MM-DD"
            return Response(err_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            age_group_stats = {}
            stat_type_list = [ 'impr_count', 'clicks_count', 'media_cost', 'data_fees', 'telco_share' ]
            for each_age_group in age_group_list:
                agegroup_stats_obj = age_stats_info.filter(age_group=each_age_group)
                for each_stat_type in stat_type_list:
                    data_dict = {}
                    data_dict["label"] = each_age_group
                    data_dict["value"] = agegroup_stats_obj.aggregate( stat_sum = Coalesce( Sum( each_stat_type ), 0 ) ).get( 'stat_sum' )
                    if each_stat_type in age_group_stats:
                        age_group_stats[ each_stat_type ].append( data_dict )
                    else:
                        age_group_stats[each_stat_type] = [ data_dict ]
            return Response( AgeStatsSerializer(age_group_stats).data )
        except:
            return Response( "Unexpected server error", status = status.HTTP_500_INTERNAL_SERVER_ERROR )