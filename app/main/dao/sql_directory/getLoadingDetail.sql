SELECT
 *
FROM
 ( SELECT * FROM bclp_bill_of_loading_no_detail_n WHERE create_time BETWEEN '{0}' AND '{1}' ) detail
 JOIN (
SELECT
 oritem_num,
 city,
 address as district,
 detail_address as unloading_address,
consig_user_name as receiving_user,
devperiod as contract_stipulates_date
FROM
 bclp_bill_of_loading_no
WHERE province like '%%山东%%' and transway like '%%汽运%%'
GROUP BY oritem_num

 ) info ON detail.oritem_num = info.oritem_num