use AR_GOA_POC;
GO

drop procedure if exists dbo.create_component;
drop procedure if exists dbo.delete_component;
GO

create procedure dbo.create_component 
		@ip_component_ID int,
		@ip_component_name varchar(256),
		@ip_component_vendor varchar(256),
		@ip_component_type varchar(256),
		@ip_component_directory varchar(256)
	
as
begin
	if @ip_component_ID not in (select component_ID from dbo.component)
	begin
		insert into dbo.component values(@ip_component_ID, @ip_component_name, @ip_component_vendor, @ip_component_type, @ip_component_directory);
	end
end
GO

create procedure dbo.delete_component 
		@ip_component_ID int
	
as
begin
	if @ip_component_ID in (select component_ID from dbo.component)
	begin
		delete from dbo.component where component_ID = @ip_component_ID;
	end
end
GO