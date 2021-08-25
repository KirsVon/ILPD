select
a.ORITEMNUM,
a.DELIWAREHOUSE,
a.`STATUS`
from
bclp_can_be_send_amount_log a,
(select
ORITEMNUM,
DELIWAREHOUSE,
max(update_time) as update_time
from
(select
ORITEMNUM,
DELIWAREHOUSE,
(CASE `STATUS`
	WHEN 'I' THEN
		CREATTIME
	ELSE
		ALTERTIME
END) as update_time
from
bclp_can_be_send_amount_log
where TRANSWAY like '汽运快运%%'
and DELIWARE in (' -','U6-黄岛库(外库)')
and DETAILADDRESS like '山东%%'
) t GROUP BY ORITEMNUM,DELIWAREHOUSE ) b
-- b表查询山东订单并且对同一订单同一出库仓库取时间最大的一条
where a.TRANSWAY like '汽运快运%%'
and a.DELIWARE in (' -','U6-黄岛库(外库)')
and a.DETAILADDRESS like '山东%%'  -- 限制山东订单
and a.ORITEMNUM = b.ORITEMNUM and a.DELIWAREHOUSE = b.DELIWAREHOUSE
and (a.CREATTIME = b.update_time or a.ALTERTIME = b.update_time) and a.`STATUS` != 'D'

