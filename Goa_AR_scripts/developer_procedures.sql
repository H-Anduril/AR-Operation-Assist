use AR_GOA_POC;
GO

drop procedure if exists dbo.count_connections;
GO

create procedure dbo.count_connections	
as
begin
	SELECT DB_NAME(dbid) AS DBName,
	COUNT(dbid) AS NumberOfConnections,
	loginame
	FROM sys.sysprocesses
	GROUP BY dbid, loginame
	ORDER BY DB_NAME(dbid)
end
GO