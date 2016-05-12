import sys
import traceback
from random import randint
import MySQLdb
from datetime import datetime, timedelta, date
import random
import pdb

status = [ "Running", "Paused", "Ended" ]
campaigns_list = [ "Demo1", "Demo2", "Demo3", "Demo4", "Demo5" ]
age_groups_list = [ "13-19", "20-30", "31-45", "46-55", "56-64", "65+" ]
gender_list = [ "Male", "Female" ]


class DBConnector:

    def __init__(self):
        self.db = MySQLdb.connect("localhost", "qa_user", "qa@password", "telco_service")


    def execute_query(self, query):
        db_cur = self.db.cursor()
        db_cur.execute( query )
        self.db.commit()


    def create_campaign_data(self, no_of_days):
        reset_camp_stats_query = """ DELETE FROM campaign_stats;"""
        self.execute_query(reset_camp_stats_query)
        for i in xrange( no_of_days ):
            for each_camp in campaigns_list:
                date_ts = (date.today()-timedelta(days=i)).isoformat()
                camp_status = random.choice( status )
                impr_count = randint( 4500, 6000 )
                clicks_count = randint( 3000, impr_count )
                media_cost = randint( 2500, 4500 )
                revenue_model = "CPM"
                payout = randint( 10000, 15000 )
                revenue = randint( payout, 2*payout )
                data_fees = randint( payout, revenue )
                telco_share = int( revenue/2 )
                telco_id = randint(1,3)
                ecpc = ( media_cost/ clicks_count )
                ecpm = ( ( media_cost * 1000 )/impr_count )
                tot_bids = randint( impr_count, 10000 )
                ctr = ( ( clicks_count*100 ) / impr_count )
                insert_query = """ INSERT INTO campaign_stats ( date_ts, name, status, impr_count, clicks_count, media_cost, revenue_model, payout, revenue, data_fees, telco_share, telco_id, ecpc, ecpm, tot_bids, ctr ) VALUES ( '%s','%s','%s',%d,%d,%d,'%s',%d,%d,%d,%d,%d,%.2f,%.2f,%d,%.2f ) """ % ( date_ts, each_camp, camp_status, impr_count,clicks_count, media_cost, revenue_model, payout, revenue, data_fees, telco_share, telco_id, ecpc, ecpm, tot_bids, ctr )
                self.execute_query( insert_query )



    def create_agestats_date(self, no_of_days):
        reset_age_stats_query = """ DELETE FROM age_stats;"""
        self.execute_query(reset_age_stats_query)
        for i in xrange(no_of_days):
            for each_age_group in age_groups_list:
                date_ts = (date.today() - timedelta(days=i)).isoformat()
                age_group = each_age_group
                impr_count = randint(50000, 80000)
                clicks_count = randint(30000, impr_count)
                media_cost = randint(10000, 15000)
                data_fees = randint(1000, 1500)
                telco_share = randint(750, 1200)
                telco_id = randint(1, 3)
                insert_query = """ INSERT INTO telco_service.age_stats ( date_ts, age_group, impr_count, clicks_count, media_cost, data_fees, telco_share, telco_id ) VALUES ('%s','%s',%d,%d,%d,%d,%d,%d) """ % (
                date_ts, age_group, impr_count, clicks_count, media_cost, data_fees, telco_share, telco_id)
                self.execute_query(insert_query)


    def create_genderstats_date(self, no_of_days):
        reset_gender_stats_query = """ DELETE FROM gender_stats;"""
        self.execute_query(reset_gender_stats_query)
        for i in xrange(no_of_days):
            for each_gender in gender_list:
                date_ts = (date.today() - timedelta(days=i)).isoformat()
                gender = each_gender
                impr_count = randint(50000, 80000)
                clicks_count = randint(30000, impr_count)
                media_cost = randint(10000, 15000)
                data_fees = randint(1000, 1500)
                telco_share = randint(750, 1200)
                telco_id = randint(1, 3)
                insert_query = """ INSERT INTO telco_service.gender_stats ( date_ts, gender, impr_count, clicks_count, media_cost, data_fees, telco_share, telco_id ) VALUES ('%s','%s',%d,%d,%d,%d,%d,%d) """ % (
                date_ts, gender, impr_count, clicks_count, media_cost, data_fees, telco_share, telco_id)
                self.execute_query(insert_query)



    def teardown(self):
        self.db.close()



if __name__ == '__main__':
    db_obj = DBConnector()
    db_obj.create_genderstats_date( 100 )
    db_obj.teardown()