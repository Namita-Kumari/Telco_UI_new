from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.db.models import Sum
from telco_service.models import *
from django.db.models.functions import Coalesce
from telco_service.serializers.genderstats_serializer import GenderStatsSerializer
import sys, pdb

class GenderStatsViewSet( viewsets.ModelViewSet ):
    model = GenderStats
    serializer_class = GenderStatsSerializer
    queryset = GenderStats.objects.all()


    def list(self, request, *args, **kwargs):
        """
        Returns Gender Stats
        """
        result = GenderStats.objects.all()
        if result:
            serializer = GenderStatsSerializer(result, many=True )
            return Response(serializer.data)
        else:
            return Response( "No Gender Statistics found", status=status.HTTP_204_NO_CONTENT )



    def retrieve(self, request,pk=None, *args, **kwargs):
        """
        Returns Gender Stats
        """
        try:
            start_date = request.query_params['start_date']
            end_date = request.query_params['end_date']
        except:
            err_msg = "Missing start date or end date both. Accepted date format : YYYY-MM-DD"
            return Response(err_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            self.gender_stats_info = GenderStats.objects.filter(date_ts__gte=start_date).filter(date_ts__lte=end_date)
            if not self.gender_stats_info:
                return Response("Age stats not found in specified date range", status=status.HTTP_204_NO_CONTENT)
        except:
            err_msg = "Invalid date. Accepted date format : YYYY-MM-DD"
            return Response(err_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        gender_stats = {}
        gender_stats['impr_data'] = self.prepare_data_set( 'impr_count' )
        gender_stats['clicks_data'] = self.prepare_data_set( 'clicks_count' )
        gender_stats['media_cost_data'] = self.prepare_data_set( 'media_cost' )
        gender_stats['data_fees_data'] = self.prepare_data_set( 'data_fees' )
        gender_stats['telco_share_data'] = self.prepare_data_set( 'telco_share' )

        return  Response( GenderStatsSerializer( gender_stats ).data )


    def prepare_data_set(self, entity ):
        entity_data = []
        male_dict = { "gender" : "Male" }
        female_dict = {"gender": "Female"}
        entity_male_data = self.gender_stats_info.filter( gender = "Male" ).aggregate( entity_male_sum = Coalesce( Sum( entity ), 0 ) ).get( 'entity_male_sum' )
        entity_female_data = self.gender_stats_info.filter(gender="Female").aggregate( entity_female_sum = Coalesce( Sum( entity ), 0 ) ).get( 'entity_female_sum' )
        male_dict["value"] = entity_male_data
        female_dict["value"] = entity_female_data
        entity_data.append( male_dict )
        entity_data.append(female_dict)
        return entity_data



