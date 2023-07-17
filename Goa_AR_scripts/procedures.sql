use AR_GOA_POC;
GO

drop procedure if exists dbo.create_component;
drop procedure if exists dbo.delete_component;
drop procedure if exists dbo.display_component;
drop procedure if exists dbo.fill_step_size;
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

create procedure dbo.display_component 

as
begin
	set NOCOUNT ON;
	declare @retval int;
	select 'Success' as response;
	select * from dbo.component;
	set @retval = 0;
	
	return @retval;
end
GO

create procedure dbo.fill_step_size
	@ip_step_ID int,
	@ip_panel_size_width float,
	@ip_panel_size_height float

as
begin
	set NOCOUNT ON;
	declare @retval int;
	if exists(select @ip_step_ID from dbo.step)
	begin
		update dbo.step
		set panel_size_width = @ip_panel_size_width, panel_size_height = @ip_panel_size_height
		where step_ID = @ip_step_ID;
		set @retval = 0;
		select 'Success' as response;
	end
	else
	begin
		set @retval = -1;
		select 'Step ID not found' as response;
	end
	return @retval;
end
GO