from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.db.models import Sum
from django.db.models.functions import Coalesce
from telco_service.models import *
from telco_service.serializers.campaign_serializer import *
import sys, pdb
from datetime import date, datetime, timedelta
import json
import traceback


class CampaignStatsViewSet( viewsets.ModelViewSet ):
    model = CampaignStats
    serializer_class = CampaignStatsSerializer
    queryset = CampaignStats.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Returns Campaign Stats
        """
        result = CampaignStats.objects.all()
        serializer = CampaignStatsSerializer(result, many=True )
        return Response(serializer.data)


    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Returns Campaign Stats
        """
        if request.query_params.get( 'entity' ):
            try:
                entity = {}
                entity['data'] = []
                entity_val = request.query_params.get( 'entity' )
                camp_data  = CampaignStats.objects.values_list( entity_val, flat= True ).distinct()
                if camp_data:
                    id = 0
                    for each_camp in camp_data:
                        id = id+1
                        entity[ 'data' ].append( { "label":each_camp, "id":id } )
                    return  Response( CampaginEntitySerializer( entity ).data )
                else:
                    return Response( "Campaigns doesn't exist. Create new campaign", status = status.HTTP_204_NO_CONTENT )
            except:
                err_msg = "Invalid entity name"
                return Response(err_msg, status.HTTP_400_BAD_REQUEST)

        else:
            try:
                start_date = request.query_params[ 'start_date' ]
                end_date = request.query_params['end_date']

                if ( start_date and end_date ):
                    result = CampaignStats.objects.filter( date_ts__gte = start_date ).filter( date_ts__lte = end_date )
                    if result:
                        serializer = CampaignStatsSerializer(result, many=True )
                    else:
                        return Response("No campaign exist in the given date range", status=status.HTTP_204_NO_CONTENT)
                else:
                    err_msg = "Missing start date or end date or both"
                    return Response( err_msg, status.HTTP_400_BAD_REQUEST )

                return Response(serializer.data)
            except:
                err_msg = "Missing start date or end date or both. Accepted date format : YYYY-MM-DD."
                return Response(err_msg, status.HTTP_400_BAD_REQUEST )



class OverllStatsViewSet( viewsets.ModelViewSet ):
    serializer_class = OverllStatsSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            start_date = request.query_params['start_date']
            end_date = request.query_params['end_date']
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        except:
            err_msg = "Missing Start date or end date or both. Accepted date format : YYYY-MM-DD."
            return Response(err_msg, status.HTTP_500_INTERNAL_SERVER_ERROR)

        camp_result_obj = CampaignStats.objects.filter(date_ts__gte=start_date).filter(date_ts__lte=end_date)
        if not camp_result_obj:
            return Response("No Data found", status=status.HTTP_204_NO_CONTENT)

        try:
            overall_stats = {}
            overall_stats['total_impr'] = camp_result_obj.aggregate( impr_count_sum = Coalesce(Sum('impr_count'), 0) ).get( 'impr_count_sum' )
            overall_stats['total_clicks'] = camp_result_obj.aggregate( clicks_count_sum = Coalesce(Sum('clicks_count'),0) ).get( 'clicks_count_sum' )
            overall_stats['total_media_cost'] = camp_result_obj.aggregate( media_cost_sum = Coalesce(Sum('media_cost'),0) ).get( 'media_cost_sum' )
            overall_stats['total_revenue'] = camp_result_obj.aggregate( revenue_sum = Coalesce(Sum('revenue'), 0) ).get( 'revenue_sum' )
            overall_stats['total_data_fees'] = camp_result_obj.aggregate( data_fees_sum = Coalesce(Sum('data_fees'), 0) ).get( 'data_fees_sum' )
            overall_stats['total_telco_share'] = camp_result_obj.aggregate( telco_share_sum = Coalesce(Sum('telco_share'), 0) ).get( 'telco_share_sum' )
            overall_stats['cumulative_bids'] = camp_result_obj.aggregate( tot_bids_sum = Coalesce(Sum('tot_bids'), 0) ).get( 'tot_bids_sum' )
            if overall_stats['cumulative_bids']:
                overall_stats['total_win_rate'] = ((overall_stats['total_impr'] * 100) / overall_stats['cumulative_bids'])
            else:
                overall_stats['cumulative_bids'] = 0
            if overall_stats['total_clicks']:
                overall_stats['total_ecpc'] = (overall_stats['total_media_cost'] / overall_stats['total_clicks'])
            else:
                overall_stats['total_ecpc'] = 0
            if overall_stats['total_impr']:
                overall_stats['total_ecpm'] = ((overall_stats['total_media_cost'] * 1000) / overall_stats['total_impr'])
                overall_stats['total_ctr'] = ((overall_stats['total_clicks'] * 100) / overall_stats['total_impr'] )
            else:
                overall_stats['total_ecpm'] = 0
                overall_stats['total_ctr'] = 0

            impr_data = [0]
            clicks_data = [0]
            media_cost_data = [0]
            data_fees_data = [0]
            telco_share_data = [0]

            delta_days = ( end_date_obj - start_date_obj ).days
            dates_list = [ '' ]
            for i in range( delta_days, -1, -1 ):
                each_date = ( end_date_obj - timedelta( days = i ) )
                dates_list.append( each_date.strftime( "%d %b" )  )
                curr_date = each_date.strftime( "%Y-%m-%d" )
                daily_camp_obj = camp_result_obj.filter( date_ts = curr_date )
                impr_data.append( daily_camp_obj.aggregate( impr_count_sum = Coalesce(Sum('impr_count'), 0) ).get( 'impr_count_sum' ) )
                clicks_data.append( daily_camp_obj.aggregate( clicks_count_sum = Coalesce(Sum('clicks_count'),0) ).get( 'clicks_count_sum' ) )
                media_cost_data.append( daily_camp_obj.aggregate( media_cost_sum = Coalesce(Sum('media_cost'),0) ).get( 'media_cost_sum' ) )
                data_fees_data.append( daily_camp_obj.aggregate( data_fees_sum = Coalesce(Sum('data_fees'), 0) ).get( 'data_fees_sum' ) )
                telco_share_data.append( daily_camp_obj.aggregate( telco_share_sum = Coalesce(Sum('telco_share'), 0) ).get( 'telco_share_sum' ) )

            overall_stats['dates_list'] = dates_list
            overall_stats['impr_data'] = [impr_data]
            overall_stats['clicks_data'] = [clicks_data]
            overall_stats['media_cost_data'] = [media_cost_data]
            overall_stats['data_fees_data'] = [data_fees_data]
            overall_stats['telco_share_data'] = [telco_share_data]

            return Response ( OverllStatsSerializer(overall_stats).data )
        except:
            return Response("Unexpected error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CampaignReportViewSet( viewsets.ModelViewSet ):
    serializer_class = CampaignReportSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            start_date = request.query_params[ 'start_date' ]
            end_date = request.query_params[ 'end_date' ]
            report_type = request.query_params['report_type']
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        except:
            err_msg = "Missing required fields. Required fields list : [ Start date, End date, Report type ] Accepted date format : YYYY-MM-DD."
            return Response(err_msg, status.HTTP_500_INTERNAL_SERVER_ERROR)

        delta_days = (end_date_obj - start_date_obj).days + 1
        dates_list = []
        for i in xrange(delta_days):
            dates_list.append((end_date_obj - timedelta(days=i)).strftime('%Y-%m-%d'))

        try:
            selected_campaigns = request.query_params[ 'selected_campaigns' ]
            if ( selected_campaigns == 'all' ):
                result = CampaignStats.objects.filter(date_ts__gte=start_date).filter(date_ts__lte=end_date)
                selected_campaigns_list =  result.values_list( 'name', flat= True ).distinct()
            else:
                selected_campaigns_list = selected_campaigns.split( ',' )
                result = CampaignStats.objects.filter(date_ts__gte=start_date).filter(date_ts__lte=end_date).filter( name__in = selected_campaigns_list )
            if not result:
                return Response( "No Data Found", status=status.HTTP_204_NO_CONTENT )

            report_overall_stats = {}
            report_overall_stats[ 'impr_count' ] = result.aggregate( impr_count_sum = Coalesce(Sum('impr_count'), 0) ).get( 'impr_count_sum' )
            report_overall_stats['clicks_count'] = result.aggregate( clicks_count_sum = Coalesce(Sum('clicks_count'),0) ).get( 'clicks_count_sum' )
            if ( report_overall_stats[ 'impr_count' ] and report_overall_stats['clicks_count'] and ( report_overall_stats[ 'impr_count' ] != 0 ) ):
                report_overall_stats['ctr'] = (( report_overall_stats['clicks_count'] * 100) / report_overall_stats[ 'impr_count' ] )
            else:
                report_overall_stats['ctr'] = 0
            report_overall_stats['media_cost'] = result.aggregate(Sum('media_cost')).get( 'media_cost__sum' )
            report_overall_stats['telco_share'] = result.aggregate(Sum('telco_share')).get( 'telco_share__sum' )

            if report_type == 'bc':
                campaign_level_report = []
                header_column_list = [ "Name", "Status", "Impressions", "Clicks", "CTR", "eCPM", "Media Cost", "Revenue Model", "Payout", "Revenue", "Data Fees", "Telco Share" ]
                for each_campaign in selected_campaigns_list:
                    filtered_campaign_obj = result.filter(name=each_campaign)
                    impr_count = filtered_campaign_obj.aggregate( impr_count_sum = Coalesce(Sum('impr_count'), 0) ).get( 'impr_count_sum' )
                    clicks_count = filtered_campaign_obj.aggregate( clicks_count_sum = Coalesce(Sum('clicks_count'),0) ).get( 'clicks_count_sum' )
                    if ( impr_count and clicks_count and ( impr_count != 0 ) ):
                        ctr = ((clicks_count * 100) / impr_count )
                    else:
                        ctr = 0
                    media_cost = filtered_campaign_obj.aggregate(Sum('media_cost')).get('media_cost__sum')
                    if ( impr_count and impr_count != 0 ):
                        ecpm = ((media_cost * 1000) / impr_count)
                    else:
                        ecpm = 0
                    revenue_model = filtered_campaign_obj[0].revenue_model
                    payout = filtered_campaign_obj[0].payout
                    camp_status = filtered_campaign_obj[0].status
                    revenue = filtered_campaign_obj.aggregate( revenue_sum = Coalesce(Sum('revenue'), 0) ).get( 'revenue_sum' )
                    data_fees = filtered_campaign_obj.aggregate( data_fees_sum = Coalesce(Sum('data_fees'), 0) ).get( 'data_fees_sum' )
                    telco_share = filtered_campaign_obj.aggregate( telco_share_sum = Coalesce(Sum('telco_share'), 0) ).get( 'telco_share_sum' )
                    report_list = [ each_campaign, camp_status, impr_count, clicks_count, ctr, ecpm, media_cost, revenue_model, payout, revenue, data_fees, telco_share ]
                    campaign_level_report.append( report_list )
                report_overall_stats[ 'entity_level_report' ] = campaign_level_report
                report_overall_stats['column_list'] = header_column_list
                return Response( CampaignReportSerializer(report_overall_stats).data )

            elif report_type == 'bd':
                date_level_report = []
                header_column_list = ["Date", "Impressions", "Clicks", "CTR", "eCPM", "Media Cost", "Revenue", "Data Fees", "Telco Share"]
                for each_date in dates_list:
                    report_list = [each_date]
                    filtered_date_obj = result.filter( date_ts=each_date )
                    if filtered_date_obj:
                        impr_count = filtered_date_obj.aggregate(Sum('impr_count')).get('impr_count__sum')
                        clicks_count = filtered_date_obj.aggregate(Sum('clicks_count')).get('clicks_count__sum')
                        if (impr_count and clicks_count and (impr_count != 0)):
                            ctr = ((clicks_count * 100) / impr_count)
                        else:
                            ctr = 0
                        media_cost = filtered_date_obj.aggregate( media_cost_sum = Coalesce( Sum('media_cost'),0) ).get( 'media_cost_sum' )
                        if (impr_count and impr_count != 0):
                            ecpm = ((media_cost * 1000) / impr_count)
                        else:
                            ecpm = 0
                        revenue = filtered_date_obj.aggregate( revenue_sum = Coalesce(Sum('revenue'), 0) ).get( 'revenue_sum' )
                        data_fees = filtered_date_obj.aggregate( data_fees_sum = Coalesce(Sum('data_fees'), 0) ).get( 'data_fees_sum' )
                        telco_share = filtered_date_obj.aggregate( telco_share_sum = Coalesce(Sum('telco_share'), 0) ).get( 'telco_share_sum' )
                        report_list.extend( [ impr_count, clicks_count, ctr, ecpm, media_cost, revenue, data_fees, telco_share ]  )
                        date_level_report.append(report_list)
                report_overall_stats['entity_level_report'] = date_level_report
                report_overall_stats['column_list'] = header_column_list
                return Response(CampaignReportSerializer(report_overall_stats).data)


            elif report_type == 'bcd':
                camp_date_level_report = []
                header_column_list = [ "Date", "Name", "Impressions", "Clicks", "CTR", "eCPM", "Media Cost", "Revenue Model", "Payout", "Revenue", "Data Fees", "Telco Share"]
                for each_obj in result:
                    report_list = [ each_obj.date_ts, each_obj.name, each_obj.impr_count, each_obj.clicks_count, each_obj.ctr, each_obj.ecpm, each_obj.media_cost, each_obj.revenue_model, each_obj.payout, each_obj.revenue, each_obj.data_fees,  each_obj.telco_share ]
                    camp_date_level_report.append( report_list )
                report_overall_stats[ 'entity_level_report' ] = camp_date_level_report
                report_overall_stats['column_list'] = header_column_list
                return Response(CampaignReportSerializer(report_overall_stats).data)

            else:
                err_msg = "Invalid report type"
                return Response(err_msg, status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            print traceback.format_exc()
            err_msg = "Unexpected error. Check the query params"
            return Response(err_msg, status.HTTP_500_INTERNAL_SERVER_ERROR)