select * from (
select
n.carmark as car_mark,
n.prod_kind_price_out as commodity,
n.trans_group_name as trans_group_name,
cast(sum(n.weight) as DECIMAL(10,3)) as weight,
n.city as city,
n.district as end_point,
n.mark as mark,
n.create_time as create_time
from(
select m.*,
(CASE
WHEN m.outstock_code like '%临港东库' THEN
'运输临港东库'
WHEN m.outstock_code like '%临港西库' THEN
'运输临港西库'
ELSE
'-'
END)as mark
from (

select carmark,main_product_list_no,notice_num,oritem_num,productlsitno,commodity_name,prod_kind_price_out,weight,count,outstock_code,create_time,trans_group_id,trans_group_name,province,city,district,detail_address,devperiod
from
(select u.*,sp.prod_kind_price_out
from(
select *
from (select b.*,c.province as province,
(
CASE
 c.city
 WHEN '胶州' THEN
 '青岛市'
 WHEN '即墨' THEN
 '青岛市'
 WHEN '安丘' THEN
 '潍坊市'
 WHEN '莱西' THEN
 '青岛市'
 WHEN '日照' THEN
 '日照市'
 WHEN '济南' THEN
 '济南市'
 WHEN '济宁' THEN
 '济宁市'
 WHEN '泰安' THEN
 '泰安市'
 WHEN '莱芜' THEN
 '莱芜市'
 WHEN '聊城' THEN
 '聊城市'
 WHEN '德州' THEN
 '德州市'
 WHEN '烟台' THEN
 '烟台市'
 WHEN '威海' THEN
 '威海市'
 WHEN '临沂' THEN
 '临沂市'
 WHEN '潍坊' THEN
 '潍坊市'
 WHEN '淄博' THEN
 '淄博市'
 WHEN '东营' THEN
 '东营市'
 WHEN '滨州' THEN
 '滨州市'
 WHEN '枣庄' THEN
 '枣庄市'
 WHEN '菏泽' THEN
 '菏泽市'
 WHEN '青岛' THEN
 '青岛市'
 ELSE c.city
END
 ) AS city,
c.address as district,c.detail_address,c.devperiod
from
(select a.*
from
(select bd.*,bm.trans_group_id,bm.trans_group_name,bm.carmark
from (
select *
FROM db_inter.bclp_bill_of_loading_no_detail_n
WHERE create_time>20190702180000 and create_time<20190702182000
and instock_code not in ( 'U%','C%')
) bd
left join (select * FROM db_inter.bclp_bill_of_loading_no_main_n
where create_time>20190702180000 and create_time<20190702182000
and trans_group_id not in ('')
and trans_group_name not in ('')
group by main_product_list_no
having count(*)=1) bm
on bm.main_product_list_no=bd.main_product_list_no)as a
where a.trans_group_id not in ('')
and a.trans_group_name not in ('')
) b
left join
(select oritem_num,province,city,address,detail_address,devperiod from db_inter.bclp_bill_of_loading_no) c
on b.oritem_num=c.oritem_num
) t
) u
left join
(select * from db_sys.vt_prod_spections
 where company_id = 'C000000882'
 and length_start = 0
and length_end = 0)as sp
on u.commodity_name=sp.prod_kind)as v
where v.province='山东省'
#and v.prod_kind_price_out='黑卷'
#where v.prod_kind_price_out='黑卷'
#and v.main_product_list_no=3190702001741
#where v.main_product_list_no=3190702001030
) m) n
where n.prod_kind_price_out in ('白卷','黑卷','螺纹','线材','型钢','开平板','窄带','冷板')
group by main_product_list_no
) l
order by l.create_time




select * from (
select
n.carmark as car_mark,
n.prod_kind_price_out as commodity,
n.trans_group_name as trans_group_name,
cast(sum(n.weight) as DECIMAL(10,3)) as weight,
n.city as city,
n.district as end_point,
n.mark as mark,
n.create_time as create_time
from(
select m.*,
(CASE
WHEN m.outstock_code like '%临港东库' THEN
'运输临港东库'
WHEN m.outstock_code like '%临港西库' THEN
'运输临港西库'
ELSE
'-'
END)as mark
from (

select carmark,main_product_list_no,notice_num,oritem_num,productlsitno,commodity_name,prod_kind_price_out,weight,count,outstock_code,create_time,trans_group_id,trans_group_name,province,city,district,detail_address,devperiod
from
(select u.*,sp.prod_kind_price_out
from(
select *
from (select b.*,c.province as province,
(
CASE
 c.city
 WHEN '胶州' THEN
 '青岛市'
 WHEN '即墨' THEN
 '青岛市'
 WHEN '安丘' THEN
 '潍坊市'
 WHEN '莱西' THEN
 '青岛市'
 WHEN '日照' THEN
 '日照市'
 WHEN '济南' THEN
 '济南市'
 WHEN '济宁' THEN
 '济宁市'
 WHEN '泰安' THEN
 '泰安市'
 WHEN '莱芜' THEN
 '莱芜市'
 WHEN '聊城' THEN
 '聊城市'
 WHEN '德州' THEN
 '德州市'
 WHEN '烟台' THEN
 '烟台市'
 WHEN '威海' THEN
 '威海市'
 WHEN '临沂' THEN
 '临沂市'
 WHEN '潍坊' THEN
 '潍坊市'
 WHEN '淄博' THEN
 '淄博市'
 WHEN '东营' THEN
 '东营市'
 WHEN '滨州' THEN
 '滨州市'
 WHEN '枣庄' THEN
 '枣庄市'
 WHEN '菏泽' THEN
 '菏泽市'
 WHEN '青岛' THEN
 '青岛市'
 ELSE c.city
END
 ) AS city,
c.address as district,c.detail_address,c.devperiod
from
(select a.*
from
(select bd.*,bm.trans_group_id,bm.trans_group_name,bm.carmark
from (
select *
FROM db_inter.bclp_bill_of_loading_no_detail_n
WHERE create_time>20190702180000 and create_time<20190702182000
and instock_code not in ( 'U%','C%')
) bd
left join (select * FROM db_inter.bclp_bill_of_loading_no_main_n
where create_time>20190702180000 and create_time<20190702182000
and trans_group_id not in ('')
and trans_group_name not in ('')
group by main_product_list_no
having count(*)=1) bm
on bm.main_product_list_no=bd.main_product_list_no)as a
where a.trans_group_id not in ('')
and a.trans_group_name not in ('')
) b
left join
(select oritem_num,province,city,address,detail_address,devperiod from db_inter.bclp_bill_of_loading_no) c
on b.oritem_num=c.oritem_num
) t
) u
left join
(select * from db_sys.vt_prod_spections
 where company_id = 'C000000882'
 and length_start = 0
and length_end = 0)as sp
on u.commodity_name=sp.prod_kind)as v
where v.province='山东省'
#and v.prod_kind_price_out='黑卷'
#where v.prod_kind_price_out='黑卷'
#and v.main_product_list_no=3190702001741
#where v.main_product_list_no=3190702001030
) m) n
where n.prod_kind_price_out in ('白卷','黑卷','螺纹','线材','型钢','开平板','窄带','冷板')
group by main_product_list_no
) l
order by l.create_time

