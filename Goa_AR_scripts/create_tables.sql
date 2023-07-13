use AR_GOA_POC;
GO

drop table if exists dbo.step_component;
drop table if exists dbo.component;
drop table if exists dbo.step;
drop table if exists dbo.operation;
drop table if exists dbo.product;

create table dbo.product (
	product_ID int NOT NULL,
	product_name varchar(256) NOT NULL,
	CONSTRAINT pk_product_ID PRIMARY KEY (product_ID)
);


create table dbo.operation (
	operation_ID int NOT NULL,
	operation_name varchar(256) NOT NULL,
	product_ID int NOT NULL,
	CONSTRAINT pk_operation_ID PRIMARY KEY (operation_ID),
	CONSTRAINT fk_product_ID FOREIGN KEY (product_ID)
		REFERENCES dbo.product(product_ID)
);


create table dbo.step (
	step_ID int NOT NULL,
	operation_ID int NOT NULL,
	panel_size_width int NOT NULL,
	panel_size_height int NOT NULL,
	CONSTRAINT pk_step_ID PRIMARY KEY (step_ID),
	CONSTRAINT fk_operation_ID FOREIGN KEY (operation_ID)
		REFERENCES dbo.operation(operation_ID)
);


create table dbo.component (
	component_ID int NOT NULL,
	component_name varchar(256) NOT NULL,
	component_vendor varchar(256),
	component_type varchar(256),
	component_directory varchar(256),
	CONSTRAINT pk_component_ID PRIMARY KEY (component_ID),
);

create table dbo.step_output (
	component_name varchar(256) NOT NULL,
	scene_width int NOT NULL,
	scene_height int NOT NULL,
	x_coord float NOT NULL,
	y_coord float NOT NULL,
	component_width float NOT NULL,
	component_height float NOT NULL,
	file_location varchar(256),
	output_id varchar(256) NOT NULL
);

create table dbo.step_component (
	step_ID int,
	component_ID int,
	component_width float,
	component_height float,
	component_x float,
	component_y float,
	CONSTRAINT pk_step_component PRIMARY KEY (step_ID, component_ID),
	CONSTRAINT fk_step_ID FOREIGN KEY (step_ID)
		REFERENCES dbo.step(step_ID),
	CONSTRAINT fk_component_ID FOREIGN KEY (component_ID)
		REFERENCES dbo.component(component_ID),
);