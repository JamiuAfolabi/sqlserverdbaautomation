SCRIPTS = [
            # Extracts names of user databases
            '''
                select name
                from sys.sysdatabases
                where 1=1
                and name not in
                ('master','tempdb','model','msdb')
            ''',
            # Extracts the size of drive
            '''
                SELECT distinct(volume_mount_point), 
                total_bytes/1048576 as Size_in_MB, 
                available_bytes/1048576 as Free_in_MB,
                (select ((available_bytes/1048576* 1.0)/(total_bytes/1048576* 1.0) *100)) as FreePercentage
                FROM sys.master_files AS f CROSS APPLY 
                sys.dm_os_volume_stats(f.database_id, f.file_id)
                group by volume_mount_point, total_bytes/1048576, 
                available_bytes/1048576 order by 4
            ''',
            # Extracts information with regards to log shipping errors
            '''
                SELECT CASE agent_type WHEN 1 THEN 'Backup' WHEN 2 THEN 'Copy' WHEN 3 THEN 'Restore' END as agent_type, * 
                from msdb..log_shipping_monitor_error_detail
                where log_time between getdate() and DATEADD(dd,-7,getdate())
            ''',
            # Extracts information with regards to Backups
            '''
             SELECT DB.name AS Database_Name
                ,MAX(DB.recovery_model_desc) AS Recovery_Model
                ,MAX(BS.backup_start_date) AS Last_Backup
                ,MAX(CASE WHEN BS.type = 'D'
                THEN BS.backup_start_date END)
                AS Last_Full_backup
                ,SUM(CASE WHEN BS.type = 'D'
                THEN 1 END)
                AS Count_Full_backup
                ,MAX(CASE WHEN BS.type = 'L'
                THEN BS.backup_start_date END)
                AS Last_Log_backup
                ,MAX(CASE WHEN BS.type = 'I'
                THEN BS.backup_start_date END)
                AS Last_Differential_backup
                FROM sys.databases AS DB
                LEFT JOIN
                msdb.dbo.backupset AS BS
                ON BS.database_name = DB.name
                WHERE 1=1 
				and database_name not in ('msdb','tempdb','master','model')
				and
				ISNULL(BS.is_damaged, 0) = 0-- exclude damaged backups
                GROUP BY DB.name
                ORDER BY Last_Backup desc

            ''',
            # Information with regards to failed jobs on the Database
            '''
                SELECT MSDB.dbo.agent_datetime(jh.run_date,jh.run_time) as date_time
                ,j.name as job_name,js.step_id as job_step,jh.message as error_message
                FROM msdb.dbo.sysjobs AS j
                INNER JOIN msdb.dbo.sysjobsteps AS js ON js.job_id = j.job_id
                INNER JOIN msdb.dbo.sysjobhistory AS jh ON jh.job_id = j.job_id AND jh.step_id = js.step_id
                WHERE jh.run_status = 0 AND MSDB.dbo.agent_datetime(jh.run_date,jh.run_time) >= GETDATE()-7
                ORDER BY MSDB.dbo.agent_datetime(jh.run_date,jh.run_time) DESC
            ''',
            # List of users on the Database
            '''
                select a.database_id,
                a.name,a.create_date,b.name,a.user_access_desc,a.state_desc,compatibility_level, recovery_model_desc, Sum((c.size*8)/1024) as DBSizeInMB
                from sys.databases a inner join sys.server_principals b on a.owner_sid=b.sid inner join sys.master_files c on a.database_id=c.database_id
                Where a.database_id>0
                Group by a.name,a.create_date,b.name,a.user_access_desc,compatibility_level,a.state_desc, recovery_model_desc,a.database_id
            ''',
            '''
                select sp.name as login,
                sp.create_date,
                --sp.type_desc as login_type,
                case when sp.is_disabled = 1 then 'Disabled'
                else 'Enabled' end as status
                from sys.server_principals sp
                left join sys.sql_logins sl
                on sp.principal_id = sl.principal_id
                left join sys.database_principals dp
                on sp.principal_id = dp.principal_id
                where sp.type not in ('A', 'G', 'R', 'X')
                and sp.type_desc not in ('CERTIFICATE_MAPPED_LOGIN')
                --and dp.type not in ( 'S', 'U', 'G' )
                and sp.name not in ('NT AUTHORITY\SYSTEM', 'NT Service\MSSQLSERVER', 'NT SERVICE\SQLSERVERAGENT','NT SERVICE\SQLWriter','NT SERVICE\Winmgmt','##MS_PolicyEventProcessingLogin##','##MS_PolicyTsqlExecutionLogin##')
                order by sp.name
            '''
            ]