use AR_GOA_POC;
GO

drop procedure if exists dbo.create_component;
drop procedure if exists dbo.delete_component;
drop procedure if exists dbo.display_component;
drop procedure if exists dbo.fill_step_size;
drop procedure if exists dbo.add_product;
drop procedure if exists dbo.add_operation;
drop procedure if exists dbo.verify_step;
drop procedure if exists dbo.add_step;
drop procedure if exists dbo.add_component;
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

create procedure dbo.add_product
	@ip_product_ID int,
	@ip_product_name varchar(256)

as
begin
	set NOCOUNT ON;
	declare @retval int;
	if @ip_product_ID in (select product_ID from dbo.product)
	begin
		select 'Product Already Exists' as response;
		set @retval = 1;
	end
	else
	begin
		insert into dbo.product values(@ip_product_ID, @ip_product_name);
		select 'Success' as response;
		set @retval = 0;
	end
	return @retval;
end
GO

create procedure dbo.add_operation
	@ip_operation_ID int,
	@ip_operation_name varchar(256),
	@ip_product_ID varchar(256)

as
begin
	set NOCOUNT ON;
	declare @retval int;
	if @ip_product_ID in (select product_ID from dbo.product)
	begin
		if @ip_operation_ID in (select operation_ID from dbo.operation)
		begin
			select 'Operation Already Exists' as response
			set @retval = 2;
		end
		else
		begin
			insert into dbo.operation values(@ip_operation_ID, @ip_product_ID, @ip_operation_name)
			select 'Success' as response;
			set @retval = 0;
		end
	end
	else
	begin
		select 'Product not Defined' as response;
		set @retval = 1;
	end
	return @retval;
end
GO

create procedure dbo.add_step
	@ip_product_ID int,
	@ip_operation_ID int,
	@ip_step_ID int,
	@ip_panel_size_width int,
	@ip_panel_size_height int,
	@ip_step_time_limit int,
	@ip_step_name varchar(256),
	@ip_scale_factor float

as
begin
	set NOCOUNT ON;
	declare @retval int;

	insert into dbo.step values(@ip_step_ID, @ip_step_name, @ip_operation_ID, @ip_product_ID,
		@ip_panel_size_width, @ip_panel_size_height, @ip_step_time_limit, @ip_scale_factor);
	select 'Success' as response;
	set @retval = 0;
	return @retval;
end
GO

create procedure dbo.add_component
	@ip_component_ID int,
	@ip_component_name varchar(256),
	@ip_component_vendor varchar(256),
	@ip_component_type varchar(256),
	@ip_component_directory varchar(256)

as
begin
	set NOCOUNT ON;
	declare @retval int;
	if @ip_component_ID not in (select component_ID from dbo.component) begin
		insert into dbo.component values(@ip_component_ID, @ip_component_name, @ip_component_vendor, @ip_component_type, @ip_component_directory);
		select 'Success' as response;
		set @retval = 0;
	end
	else begin
		select 'Component Already Exists' as response;
		set @retval = 1;
	end
end
GO

create procedure dbo.display_component 

as
begin
	set NOCOUNT ON;
	declare @retval int;
	select * from dbo.component;
	select 'Success' as response;
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
	if @ip_step_ID in (select step_ID from dbo.step)
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

create procedure dbo.verify_step
	@ip_product_ID int,
	@ip_operation_ID int,
	@ip_step_ID int

as
begin
	set NOCOUNT ON;
	declare @retval int;

	if @ip_product_ID in (select product_ID from dbo.operation)
	begin
		if @ip_operation_ID in (select operation_ID from dbo.operation where product_ID = @ip_product_ID)
		begin
			if @ip_step_ID not in (select step_ID from dbo.step where product_ID = @ip_product_ID and operation_ID = @ip_operation_ID)
			begin
				set @retval = 0;
				select 'Valid Step ID' as response;
			end
			else begin
				set @retval = 1;
				select 'Step ID Already Exists' as response;
			end
		end
		else begin
			set @retval = 2;
			select 'Operation not Exist' as response;
		end
	end
	else begin
		set @retval = 3;
		select 'Product not Exist' as response;
	end
	return @retval;
end
GO