use AR_GOA_POC;
GO


select
	ROUTINE_SCHEMA,
	ROUTINE_NAME
from INFORMATION_SCHEMA.ROUTINES
where ROUTINE_TYPE = 'PROCEDURE'

select * from dbo.component;

insert into dbo.component values(-1, 'test component', 'test vendor', 'test type', '/')