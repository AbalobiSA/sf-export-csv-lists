SELECT trip_date__c, SUM(cost_bait__c) cost_bait, SUM(cost_food__c) cost_food, SUM(cost_fuel__c) cost_fuel, SUM(cost_harbour_fee__c) cost_harbour_fee, SUM(cost_oil__c) cost_oil, SUM(cost_other_amount__c) cost_other, SUM(cost_transport__c) cost_transport, SUM(displayed_profit__c) displayed_profit FROM Ablb_Fisher_Trip__c WHERE cost_has__c ='yes' AND trip_date__c > 2016-10-31 GROUP BY trip_date__c ORDER BY trip_date__c ASC NULLS FIRST

SELECT trip_date__c FROM Ablb_Fisher_Trip__c WHERE cost_has__c ='yes' AND trip_date__c > 2016-10-31 GROUP BY trip_date__c ORDER BY trip_date__c ASC NULLS FIRST

SELECT trip_date__c, main_fisher_id__c, SUM(cost_bait__c) cost_bait, SUM(cost_food__c) cost_food, SUM(cost_fuel__c) cost_fuel, SUM(cost_harbour_fee__c) cost_harbour_fee, SUM(cost_oil__c) cost_oil, SUM(cost_other_amount__c) cost_other, SUM(cost_transport__c) cost_transport, SUM(displayed_profit__c) displayed_profit FROM Ablb_Fisher_Trip__c WHERE cost_has__c ='yes' AND trip_date__c > 2016-10-31 GROUP BY trip_date__c, main_fisher_id__c ORDER BY trip_date__c, main_fisher_id__c ASC NULLS FIRST


//NIKLAAS

SELECT trip_date__c, main_fisher_id__c, cost_bait__c displayed_profit__c FROM Ablb_Fisher_Trip__c WHERE cost_has__c ='yes' AND trip_date__c > 2016-10-31 AND main_fisher_id__c='niklaas' GROUP BY trip_date__c, main_fisher_id__c ORDER BY trip_date__c, main_fisher_id__c ASC NULLS FIRST

SELECT trip_date__c, main_fisher_id__c, SUM(cost_bait__c) cost_bait, SUM(cost_food__c) cost_food, SUM(cost_fuel__c) cost_fuel, SUM(cost_harbour_fee__c) cost_harbour_fee, SUM(cost_oil__c) cost_oil, SUM(cost_other_amount__c) cost_other, SUM(cost_transport__c) cost_transport, SUM(displayed_profit__c) displayed_profit FROM Ablb_Fisher_Trip__c WHERE cost_has__c ='yes' AND trip_date__c > 2016-10-31 GROUP BY trip_date__c, main_fisher_id__c ORDER BY trip_date__c, main_fisher_id__c ASC NULLS FIRST


===================================================================================================
Returns all trips for november

SELECT trip_date__c, main_fisher_id__c, cost_bait__c, cost_food__c, cost_fuel__c, cost_harbour_fee__c, cost_oil__c, cost_other_amount__c, cost_transport__c, displayed_profit__c FROM Ablb_Fisher_Trip__c WHERE cost_has__c ='yes' AND trip_date__c > 2016-10-31 ORDER BY trip_date__c, main_fisher_id__c ASC NULLS FIRST

===================================================================================================
Returns all catches for november

SELECT trip_date__c, main_fisher_id__c, cost_bait__c, cost_food__c, cost_fuel__c, cost_harbour_fee__c, cost_oil__c, cost_other_amount__c, cost_transport__c, displayed_profit__c FROM Ablb_Fisher_Catch__c WHERE cost_has__c ='yes' AND trip_date__c > 2016-10-31 ORDER BY trip_date__c, main_fisher_id__c ASC NULLS FIRST