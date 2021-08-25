select
ORITEMNUM,
DELIWAREHOUSE
from
bclp_can_be_send_amount_log
where `STATUS` = 'D'
and TRANSWAY like '汽运快运%%'
and DELIWARE in (' -','U6-黄岛库(外库)')
and DETAILADDRESS like '山东%%'