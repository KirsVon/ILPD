select
a.DELIWAREHOUSE as out_stock,
a.ORITEMNUM as order_number,
a.CANSENDWEIGHT as can_send_weight,
a.CANSENDNUMBER as can_send_count,
a.ALTERTIME as AlTERTIME,
a.COMMODITYNAME as commodity,
a.PROVINCE as PROVINCE,
c.CITY as city,
c.ADDRESS as district,
a.DETAILADDRESS as unloading_address,
a.PURCHUNIT as receiving_user,
a.devperiod as contract_stipulates_date,
a.NOTICENUM as shipping_order,
a.STANDARD as specifications

                from
                db_inter.bclp_can_be_send_amount_log a,
                (select
                ORITEMNUM,
                DELIWAREHOUSE,
                NOTICENUM,
                max(update_time) as update_time
                from
                (select
                ORITEMNUM,
                DELIWAREHOUSE,
                NOTICENUM,
                (case `STATUS`
                WHEN 'I' THEN
                CREATTIME
                else
                ALTERTIME
                end) as update_time
                from
                db_inter.bclp_can_be_send_amount_log
                where TRANSWAY like '汽运快运%%'
                and DELIWARE in (' -','U6-黄岛库(外库)')
                and DETAILADDRESS like '山东%%'
                ) t
                where t.update_time <= '{0}'
                group by t.ORITEMNUM,t.NOTICENUM,t.DELIWAREHOUSE ) b,
								(
								select
								city,
								address,
								oritem_num
								from
								db_inter.bclp_bill_of_loading_no
							  group by oritem_num )	c
                -- b表查询山东订单并且对同一订单同一出库仓库取时间最大的一条
                where a.TRANSWAY = '汽运快运'
                and a.DELIWARE in (' -','U6-黄岛库(外库)')
                and a.DETAILADDRESS like '山东%%'  -- 限制山东订单
                and a.ORITEMNUM = b.ORITEMNUM
                and a.DELIWAREHOUSE = b.DELIWAREHOUSE
                and a.NOTICENUM = b.NOTICENUM
                and (a.CREATTIME = b.update_time or a.ALTERTIME = b.update_time) and a.`STATUS` != 'D'
                and IFNULL(a.ALTERTIME, a.CREATTIME) <= '{0}' and a.CANSENDWEIGHT > '0'
								and a.ORITEMNUM = c.oritem_num
