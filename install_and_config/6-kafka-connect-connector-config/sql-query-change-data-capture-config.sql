
-- Refer Confluent Link for CDC Setup : https://docs.confluent.io/kafka-connectors/debezium-sqlserver-source/current/overview.html
 
---- Enable CDC in SQL Server ---
USE TRYIT
GO
EXEC sys.sp_cdc_enable_db
GO

------ Create Table -------

CREATE TABLE [dbo].[TestCacheKafkaConnect]
(
Id int IDENTITY(1,1) PRIMARY KEY,
RedisKey		varchar(100) ,
RedisValue varchar(max)	   ,
CreatedDate datetime2
)

---- Enable CDC on Table----
EXEC sys.sp_cdc_enable_table @source_schema = N'dbo', @source_name = N'TestCacheKafkaConnect', @role_name = NULL, @supports_net_changes = 0
GO

-------- Insert Data -----------
INSERT [dbo].[TestCacheKafkaConnect] ([RedisKey], [RedisValue], [CreatedDate]) VALUES (N'A/B/C', N'{A:1, B:2, C:3}', CAST(N'2024-04-16T21:04:39.3766667' AS DateTime2))
GO
INSERT [dbo].[TestCacheKafkaConnect] ([RedisKey], [RedisValue], [CreatedDate]) VALUES (N'L/B/C', N'{L:11, B:2, C:3}', CAST(N'2024-04-16T21:04:39.3766667' AS DateTime2))
GO
INSERT [dbo].[TestCacheKafkaConnect] ([RedisKey], [RedisValue], [CreatedDate]) VALUES (N'L/Q/C', N'{L:11, Q:2, C:3}', CAST(N'2024-04-16T21:04:39.3766667' AS DateTime2))
GO
INSERT [dbo].[TestCacheKafkaConnect] ([RedisKey], [RedisValue], [CreatedDate]) VALUES (N'L/Q/P', N'{L:11, Q:2, P:33}', CAST(N'2024-04-16T21:04:39.3766667' AS DateTime2))
GO
INSERT [dbo].[TestCacheKafkaConnect] ([RedisKey], [RedisValue], [CreatedDate]) VALUES (N'Jerin', N'{Sam}', CAST(N'2024-04-17T14:09:44.7066667' AS DateTime2))
GO
INSERT [dbo].[TestCacheKafkaConnect] ([RedisKey], [RedisValue], [CreatedDate]) VALUES (N'Aayush', N'{Tom Cru}', CAST(N'2024-04-17T14:09:44.7066667' AS DateTime2))
GO
INSERT [dbo].[TestCacheKafkaConnect] ([RedisKey], [RedisValue], [CreatedDate]) VALUES (N'Sachin', N'{Batman}', CAST(N'2024-04-17T14:09:44.7066667' AS DateTime2))
GO
INSERT [dbo].[TestCacheKafkaConnect] ([RedisKey], [RedisValue], [CreatedDate]) VALUES (N'API1', N'{DSS}', CAST(N'2024-04-17T14:11:03.5433333' AS DateTime2))
GO
INSERT [dbo].[TestCacheKafkaConnect] ([RedisKey], [RedisValue], [CreatedDate]) VALUES (N'API2', N'{TSS}', CAST(N'2024-04-17T14:11:03.5433333' AS DateTime2))
GO
INSERT [dbo].[TestCacheKafkaConnect] ([RedisKey], [RedisValue], [CreatedDate]) VALUES (N'API3', N'{DataS}', CAST(N'2024-04-17T14:11:03.5433333' AS DateTime2))
GO
INSERT [dbo].[TestCacheKafkaConnect] ([RedisKey], [RedisValue], [CreatedDate]) VALUES (N'API11', N'{A1-DSS}', CAST(N'2024-04-17T14:11:03.5433333' AS DateTime2))
GO
INSERT [dbo].[TestCacheKafkaConnect] ([RedisKey], [RedisValue], [CreatedDate]) VALUES (N'API12', N'{A1-TSS}', CAST(N'2024-04-17T14:11:03.5433333' AS DateTime2))
GO
INSERT [dbo].[TestCacheKafkaConnect] ([RedisKey], [RedisValue], [CreatedDate]) VALUES (N'API13', N'{A1-DataS}', CAST(N'2024-04-17T14:11:03.5433333' AS DateTime2))
GO
