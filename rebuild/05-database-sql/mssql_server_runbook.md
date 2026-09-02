# Phase 5: Microsoft SQL Server 2022 Database Rebuild

## 1. Node Identity
* **IP Address**: `192.168.0.237`
* **Hostname**: `sql.home`
* **OS**: Windows Server 2022 / 2025 Standard
* **RDBMS**: Microsoft SQL Server 2022 Standard / Enterprise

## 2. Network & Port Configuration
* **Default Port**: TCP `1433`
* **SQL Browser Service**: UDP `1434`
* **Firewall Rules**: Inbound rules for SQL Server TCP 1433 enabled.

## 3. Provisioning & Database Setup
Execute via SQL Server Management Studio (SSMS) or `sqlcmd`:
```sql
-- Initial Database & User Creation Runbook
CREATE DATABASE HomelabTelemetry;
GO

USE HomelabTelemetry;
GO

CREATE TABLE SubnetTrafficHistory (
    Id BIGINT IDENTITY(1,1) PRIMARY KEY,
    Timestamp DATETIME2 DEFAULT SYSUTCDATETIME(),
    SourceIP VARCHAR(45) NOT NULL,
    DestinationIP VARCHAR(45) NOT NULL,
    SourceHostname VARCHAR(255),
    DestinationHostname VARCHAR(255),
    Protocol VARCHAR(20),
    Port INT,
    ByteCount BIGINT
);
GO

CREATE INDEX IX_SubnetTraffic_IP ON SubnetTrafficHistory (SourceIP, DestinationIP);
GO
```
