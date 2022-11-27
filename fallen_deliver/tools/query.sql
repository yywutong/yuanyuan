# 查看是否有已存在的提测单
SELECT
	a.work_order id,
	jt.app,
	jt.version,
	a.form_data ->> '$.textarea_remark_id' textarea_remark 
FROM
	p_work_order_tpl_data a,
	p_work_order_info b,
	JSON_TABLE ( form_data, '$.subform_version_info_id[*]' COLUMNS ( app VARCHAR ( 50 ) PATH '$.input_deploy_app_id', version VARCHAR ( 50 ) PATH '$.input_deploy_release_version_id' ) ) AS jt 
WHERE
	a.wotype = 1 
	AND a.work_order = b.id 
	AND b.is_end = 0 
	AND JSON_CONTAINS ( b.state, '{\"label\": \"QATesting\"}' ) 
	AND jt.app = 'resource-manager-backend'

# 统计提测关联的各开发的修复单
SELECT DISTINCT
	b.nick_name,
	count( 1 ) 
FROM
	p_work_order_info a,
	sys_user b 
WHERE
	a.creator = b.user_id 
	AND a.wotype = 2 
	AND a.process = 13 
	AND a.create_time >= '2021-09-17 20:27:51' 
	AND a.create_time <= '2021-10-15 20:28:06' 
GROUP BY
	b.nick_name;