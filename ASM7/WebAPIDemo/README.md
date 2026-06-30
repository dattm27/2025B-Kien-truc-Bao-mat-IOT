# WebAPIDemo

ASP.NET Core Web API lưu dữ liệu cảm biến (SensorData) vào **MongoDB**.
Dự án được hoàn thiện theo tài liệu *WebAPI Tutorial VSCode*.

## Yêu cầu

- [.NET SDK 8.0+](https://dotnet.microsoft.com/download)
- MongoDB chạy tại `mongodb://localhost:27017`
  - Cài sẵn trên máy, hoặc chạy bằng Docker:
    ```bash
    docker run -d -p 27017:27017 --name mongodb mongo
    ```

## Cấu trúc project

```
WebAPIDemo/
├── Controllers/
│   └── SensorDatasController.cs   # CRUD API
├── Models/
│   ├── SensorData.cs              # Model + ánh xạ BSON
│   └── MongoDbSettings.cs         # Cấu hình MongoDB
├── Services/
│   └── SensorDataService.cs       # Tầng truy cập MongoDB
├── Program.cs                     # Cấu hình DI + Swagger
├── appsettings.json               # Chứa "MongoDbSettings"
└── WebAPIDemo.csproj
```

## Chạy project

```bash
cd WebAPIDemo
dotnet restore
dotnet build
dotnet run
```

Mở Swagger: <http://localhost:5050/swagger>

## Các API

| Method | API                      | Chức năng                       |
| ------ | ------------------------ | ------------------------------- |
| GET    | /api/AppVersion          | Lấy version app                 |
| POST   | /api/PostVersion         | Gửi version từ thiết bị         |
| GET    | /api/SensorDatas         | Lấy danh sách dữ liệu cảm biến  |
| GET    | /api/SensorDatas/{id}    | Lấy dữ liệu theo ID             |
| POST   | /api/SensorDatas         | Thêm dữ liệu cảm biến           |
| PUT    | /api/SensorDatas/{id}    | Cập nhật dữ liệu                |
| DELETE | /api/SensorDatas/{id}    | Xóa dữ liệu                     |

## Test bằng curl

Thêm dữ liệu:

```bash
curl -X POST http://localhost:5050/api/SensorDatas \
  -H "Content-Type: application/json" \
  -d "{\"deviceId\":\"DEVICE_001\",\"temperature\":30.5,\"humidity\":70.2}"
```

Lấy danh sách dữ liệu:

```bash
curl http://localhost:5050/api/SensorDatas
```

Dữ liệu được lưu trong MongoDB tại Database `WebAPIDemoDb`, Collection `SensorData`.
