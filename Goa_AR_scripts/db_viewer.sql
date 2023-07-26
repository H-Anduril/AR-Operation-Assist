use AR_GOA_POC;
GO


select
	ROUTINE_SCHEMA,
	ROUTINE_NAME
from INFORMATION_SCHEMA.ROUTINES
where ROUTINE_TYPE = 'PROCEDURE'

select * from dbo.step_component;

select * from dbo.component;

insert into dbo.component values(-1, 'test component', 'test vendor', 'test type', '/')

insert into dbo.product values(-1, -1)

insert into dbo.operation values(2, -1, -1)

if 1 in (select step_ID from dbo.step where product_ID = 1 and operation_ID = 2) begin
	select 1;
end

select * from dbo.step;

insert into dbo.step values(1, '1', 5, 10, -1, -1, 1, 1);

declare @return_value int;
EXECUTE @return_value = get_component '10';
select 'Return Value' = @return_value;