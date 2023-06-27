use AR_GOA_POC;
GO

--insert into dbo.component values(-1, 'TEST', 'TEST_VENDOR', 'TEST_IMAGE', '/user/documents');

EXECUTE dbo.create_component -2, N'TEST', N'TEST_VENDOR', N'TEST_IMAGE', N'/user/documents';
GO