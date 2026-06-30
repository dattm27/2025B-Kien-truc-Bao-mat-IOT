using Microsoft.Extensions.Options;
using MongoDB.Driver;
using WebAPIDemo.Models;

namespace WebAPIDemo.Services
{
    public class SensorDataService
    {
        private readonly IMongoCollection<SensorData> _sensorDataCollection;

        public SensorDataService(IOptions<MongoDbSettings> mongoDbSettings)
        {
            var mongoClient = new MongoClient(
                mongoDbSettings.Value.ConnectionString
            );

            var mongoDatabase = mongoClient.GetDatabase(
                mongoDbSettings.Value.DatabaseName
            );

            _sensorDataCollection = mongoDatabase.GetCollection<SensorData>(
                mongoDbSettings.Value.CollectionName
            );
        }

        public async Task<List<SensorData>> GetAsync()
        {
            return await _sensorDataCollection.Find(_ => true).ToListAsync();
        }

        public async Task<SensorData?> GetAsync(string id)
        {
            return await _sensorDataCollection
                .Find(x => x.Id == id)
                .FirstOrDefaultAsync();
        }

        public async Task CreateAsync(SensorData sensorData)
        {
            await _sensorDataCollection.InsertOneAsync(sensorData);
        }

        public async Task UpdateAsync(string id, SensorData sensorData)
        {
            await _sensorDataCollection.ReplaceOneAsync(x => x.Id == id, sensorData);
        }

        public async Task RemoveAsync(string id)
        {
            await _sensorDataCollection.DeleteOneAsync(x => x.Id == id);
        }
    }
}
