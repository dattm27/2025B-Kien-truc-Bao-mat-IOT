using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace WebAPIDemo.Models
{
    public class SensorData
    {
        [BsonId]
        [BsonRepresentation(BsonType.ObjectId)]
        public string? Id { get; set; }

        public string DeviceId { get; set; } = string.Empty;

        public double Temperature { get; set; }

        public double Humidity { get; set; }

        public DateTime CreatedAt { get; set; } = DateTime.Now;
    }
}
