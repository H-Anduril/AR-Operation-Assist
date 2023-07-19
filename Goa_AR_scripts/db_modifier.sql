use AR_GOA_POC;
GO



--EXECUTE dbo.create_component -2, N'TEST', N'TEST_VENDOR', N'TEST_IMAGE', N'/user/documents';
--GO

-- EXECUTE display_component;

-- select 1 as response;

--insert into dbo.product values(-1, 'test product');
--insert into dbo.operation values(-1, 'test operation', -1);

--insert into dbo.step values(-1, -1, 800, 600);
-- select * from dbo.step
declare @return_value int;
EXECUTE @return_value = add_product '10', 'test';
select 'Return Value' = @return_value;

select TABLE_NAME from INFORMATION_SCHEMA.TABLES
where TABLE_NAME not like '%sys%';

select * from dbo.product;