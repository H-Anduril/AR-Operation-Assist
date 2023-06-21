use AR_GOA_POC
GO

create table dbo.product (
	productid int IDENTITY(1, 1) NOT NULL
		constraint pk_product_productid PRIMARY KEY,
	product_name varchar(256) NOT NULL,

);