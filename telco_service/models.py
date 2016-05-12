from django.db import models

# Create your models here.

class CampaignStats( models.Model ):
    date_ts = models.DateField(auto_now=False)
    name = models.CharField( max_length=100 )
    status = models.CharField( max_length=30 )
    impr_count = models.IntegerField()
    clicks_count = models.IntegerField()
    media_cost = models.IntegerField()
    revenue_model = models.CharField( max_length=10 )
    payout = models.IntegerField()
    revenue = models.IntegerField()
    data_fees = models.IntegerField()
    telco_share = models.IntegerField()
    telco_id = models.IntegerField()
    ecpc = models.FloatField()
    ecpm = models.FloatField()
    tot_bids = models.IntegerField()
    ctr = models.FloatField()

    class Meta:
        db_table = 'campaign_stats'


class GenderStats( models.Model ):
    date_ts = models.DateField(auto_now=False)
    gender = models.CharField( max_length=10 )
    impr_count = models.IntegerField()
    clicks_count = models.IntegerField()
    media_cost = models.IntegerField()
    data_fees = models.IntegerField()
    telco_share = models.IntegerField()
    telco_id = models.IntegerField()

    class Meta:
        db_table = 'gender_stats'


class AgeStats( models.Model ):
    date_ts = models.DateField(auto_now=False)
    age_group = models.CharField( max_length=10 )
    impr_count = models.IntegerField()
    clicks_count = models.IntegerField()
    media_cost = models.IntegerField()
    data_fees = models.IntegerField()
    telco_share = models.IntegerField()
    telco_id = models.IntegerField()

    class Meta:
        db_table = 'age_stats'

