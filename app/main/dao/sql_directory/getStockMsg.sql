select
t1.PURCHUNIT as receiving_user,
t1.DEVPERIOD  as contract_stipulates_date,
t1.NOTICENUM as shipping_order,
t1.ORITEMNUM as order_number,
t1.DELIWAREHOUSE as out_stock,
t1.TRANSWAY ,
t1.COMMODITYNAME as commodity,
t1.MATERIAL as quantity,
t1.STANDARD as specifications,
t2.address as district,
t1.DETAILADDRESS as unloading_address,
t2.city as city,
t1.CANSENDNUMBER as can_send_count,
t1.CANSENDWEIGHT as can_send_weight
from
(select
NOTICENUM,
PURCHUNIT,
ENDCUSTMER,
DEVPERIOD,
ORITEMNUM,
DELIWAREHOUSE,
TRANSWAY,
COMMODITYNAME,
QUALITY,
MATERIAL,
STANDARD,
DETAILADDRESS,
CANSENDNUMBER,
CANSENDWEIGHT
from
db_inter.bclp_can_be_send_amount
where
      STATUS != 'D'
      and TRANSWAY like '汽运快运%%'
      and CANSENDWEIGHT >'0'
      and DELIWARE in (' -','U6-黄岛库(外库)')) t1
join (
select
oritem_num,
address,
province,
city
from
db_inter.bclp_bill_of_loading_no where province like '山东%%'
GROUP BY oritem_num
) t2 on t1.ORITEMNUM = t2.oritem_num